from __future__ import annotations

import datetime as dt
from typing import Any

from peewee_aio import AIOModel, fields

from summary import db, together_ai, youtube


@db.register
class Video(AIOModel):
    id = fields.CharField(primary_key=True)

    summary_updated = fields.DateTimeField(null=True)
    captions_updated = fields.DateTimeField(null=True)

    async def update_captions(self):
        if not self.captions_updated:
            res = await youtube.get_captions(self.id)
            self.captions_updated = dt.datetime.now(tz=dt.timezone.utc)
            await self.save()

            return (
                await Caption.insert_many(
                    [
                        {
                            "video": self,
                            "language": item["language"],
                            "auto_generated": item["auto_generated"],
                            "url": item["url"],
                        }
                        for item in res
                    ]
                )
                .on_conflict(
                    conflict_target=(Caption.video, Caption.language),
                    update={Caption.url: Caption.url},
                )
                .returning(Caption)
            )

        return await self.captions


@db.register
class Caption(AIOModel):
    id = fields.AutoField(primary_key=True)
    language = fields.CharField()
    url = fields.CharField()
    auto_generated = fields.BooleanField()

    data: fields.GenericField[list[dict[str, Any]]] = db.JSONField(null=True)

    video = fields.ForeignKeyField(Video, backref="captions")

    class Meta:
        indexes = ((("video", "language"), True),)

    async def download(self):
        if self.data is None:
            self.data = await youtube.download_caption(self.url)
            await self.save()

        return self.data

    @property
    def text(self):
        return "\n".join(item["text"] for item in self.data)


@db.register
class Summary(AIOModel):
    id = fields.AutoField(primary_key=True)
    language = fields.CharField()

    title = fields.TextField()
    summary = fields.TextField()
    keynotes = fields.TextField()

    video = fields.ForeignKeyField(Video, backref="summaries")

    class Meta:
        indexes = ((("video", "language"), True),)

    @classmethod
    def parse(cls, text: str):
        head, _, summary = text.partition("\n\n**Summary:**")
        head, _, keynotes = head.partition("\n\n**Bullet Points:**")
        title = head[len("**Title:** ") :]

        return {
            "title": title.strip(),
            "summary": summary.strip(),
            "keynotes": keynotes.strip(),
        }

    @classmethod
    async def generate(cls, caption: Caption):
        text_8kb = caption.text[:8000]
        promt = f"Write a title, 5 bullet points and summary for the following text: {text_8kb}"
        res = await together_ai.api.chat.completions.post(
            raise_for_status=False,
            json={
                "model": "meta-llama/Llama-3-8b-chat-hf",
                "messages": [{"role": "system", "content": promt}],
            },
        )

        content = res["choices"][0]["message"]["content"]
        # Parse result
        return await cls.create(
            video=caption.video_id,
            language=caption.language,
            **cls.parse(content),
        )

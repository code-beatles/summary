from __future__ import annotations

from peewee_aio import AIOModel, fields

from summary import db, youtube


@db.register
class Video(AIOModel):
    id = fields.CharField(primary_key=True)

    summary_updated = fields.DateTimeField(null=True)
    captions_updated = fields.DateTimeField(null=True)

    async def update_captions(self):
        if not self.captions_updated:
            res = await youtube.get_captions(self.id)
            items = res["items"]
            return (
                await Caption.insert_many(
                    [
                        {
                            "video": self,
                            "id": item["id"],
                            "language": item["snippet"]["language"],
                            "auto_generated": item["snippet"]["trackKind"].lower()
                            == "asr",
                        }
                        for item in items
                    ]
                )
                .on_conflict_ignore()
                .returning(Caption)
            )

        return self.captions


@db.register
class Caption(AIOModel):
    id = fields.CharField(primary_key=True)
    language = fields.CharField()
    auto_generated = fields.BooleanField()
    text = fields.TextField(null=True)

    video = fields.ForeignKeyField(Video, backref="captions")

    class Meta:
        indexes = ((("video", "language"), True),)

    async def download(self):
        if self.text is None:
            self.text = await youtube.get_caption(self.id)
            await self.save()

        return self.text


@db.register
class Summary(AIOModel):
    id = fields.AutoField(primary_key=True)
    text = fields.TextField()
    language = fields.CharField()

    video = fields.ForeignKeyField(Video, backref="summaries")

    class Meta:
        indexes = ((("video", "language"), True),)

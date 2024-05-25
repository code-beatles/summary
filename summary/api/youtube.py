from __future__ import annotations

from muffin_rest import APIError, PWRESTHandler

from summary.models import Caption, Summary, Video
from summary.models.schemas import CaptionSchema, SummarySchema

from . import api


@api.route("/youtube/{id}")
class YouTube(PWRESTHandler):
    class Meta:  # type: ignore[]
        model = Video

    async def prepare_resource(self, request):
        video_id = request["path_params"]["id"]
        video, _ = await Video.get_or_create(id=video_id)
        return video

    @PWRESTHandler.route("/youtube/{id}/captions")
    async def captions(self, request, resource: Video):
        captions = await resource.update_captions()
        return CaptionSchema(many=True).dump(captions)

    @PWRESTHandler.route("/youtube/{id}/captions/{caption_id}")
    async def caption(self, request, resource: Video):
        caption = await Caption.get_or_none(
            Caption.id == request["path_params"]["caption_id"]
        )
        if caption is None:
            raise APIError.NOT_FOUND("Caption not found")

        await caption.download()
        return CaptionSchema().dump(caption)

    @PWRESTHandler.route("/youtube/{id}/summary")
    async def summary(self, request, resource: Video):
        summary = await resource.summaries.first()
        if summary is None:
            summary = await Summary.generate(resource.captions)
        return SummarySchema().dump(summary)

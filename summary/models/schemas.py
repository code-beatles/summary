from __future__ import annotations

from marshmallow_peewee import ModelSchema

from summary.models import Caption


class CaptionSchema(ModelSchema):
    class Meta:  # type: ignore[]
        model = Caption

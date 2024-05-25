from __future__ import annotations

from marshmallow_peewee import ModelSchema

from summary.models import Caption, Summary


class CaptionSchema(ModelSchema):
    class Meta:  # type: ignore[]
        model = Caption


class SummarySchema(ModelSchema):
    class Meta:  # type: ignore[]
        model = Summary

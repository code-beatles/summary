"""Peewee migrations -- 001_initial.py.

Some examples (model - class or model name)::

    > Model = migrator.orm['table_name']            # Return model in current state by name
    > Model = migrator.ModelClass                   # Return model in current state by name

    > migrator.sql(sql)                             # Run custom SQL
    > migrator.run(func, *args, **kwargs)           # Run python function with the given args
    > migrator.create_model(Model)                  # Create a model (could be used as decorator)
    > migrator.remove_model(model, cascade=True)    # Remove a model
    > migrator.add_fields(model, **fields)          # Add fields to a model
    > migrator.change_fields(model, **fields)       # Change fields
    > migrator.remove_fields(model, *field_names, cascade=True)
    > migrator.rename_field(model, old_field_name, new_field_name)
    > migrator.rename_table(model, new_table_name)
    > migrator.add_index(model, *col_names, unique=False)
    > migrator.add_not_null(model, *field_names)
    > migrator.add_default(model, field_name, default)
    > migrator.add_constraint(model, name, sql)
    > migrator.drop_index(model, *col_names)
    > migrator.drop_not_null(model, *field_names)
    > migrator.drop_constraints(model, *constraints)

"""
from __future__ import annotations

from contextlib import suppress

import peewee as pw
from peewee_migrate import Migrator

with suppress(ImportError):
    import playhouse.postgres_ext as pw_pext


def migrate(migrator: Migrator, database: pw.Database, *, fake=False):
    """Write your migrations here."""

    @migrator.create_model
    class Video(pw.Model):
        id = pw.CharField(max_length=255, primary_key=True)
        summary_updated = pw.DateTimeField(null=True)
        captions_updated = pw.DateTimeField(null=True)

        class Meta:
            table_name = "video"

    @migrator.create_model
    class Caption(pw.Model):
        id = pw.AutoField()
        language = pw.CharField(max_length=255)
        url = pw.CharField(max_length=255)
        auto_generated = pw.BooleanField()
        data = pw_pext.JSONField(null=True)
        video = pw.ForeignKeyField(
            column_name="video_id", field="id", model=migrator.orm["video"]
        )

        class Meta:
            table_name = "caption"
            indexes = [(("video", "language"), True)]

    @migrator.create_model
    class Summary(pw.Model):
        id = pw.AutoField()
        language = pw.CharField(max_length=255)
        title = pw.TextField()
        summary = pw.TextField()
        keynotes = pw.TextField()
        video = pw.ForeignKeyField(
            column_name="video_id", field="id", model=migrator.orm["video"]
        )

        class Meta:
            table_name = "summary"
            indexes = [(("video", "language"), True)]


def rollback(migrator: Migrator, database: pw.Database, *, fake=False):
    """Write your rollback migrations here."""

    migrator.remove_model("summary")
    migrator.remove_model("caption")
    migrator.remove_model("video")

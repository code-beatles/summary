from __future__ import annotations

import logging

import pytest

logger = logging.getLogger("tests")
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler())


@pytest.fixture(scope="session")
def aiolib():
    """Disable uvloop for tests (to prevent BlockingIOError)"""
    return ("asyncio", {"use_uvloop": False})


@pytest.fixture(autouse=True)
async def setup_tests(app):
    """Rollback the database between tests."""
    from summary import db

    async with db.transaction() as trans:
        logger.info("")
        yield db
        await trans.rollback()


@pytest.fixture()
async def video():
    from summary.models import Video

    return await Video.create(id="gqaHkPEZAew")


@pytest.fixture()
async def captions(video):
    from summary.models import Caption

    return await Caption.insert_many(
        [
            {
                "video": video,
                "id": "AUieDaZw0jhOuuItR-Llp7MoNGcsSJiJg9f6nCOBT5aFhgPL_40",
                "language": "en",
                "auto_generated": True,
            },
            {
                "video": video,
                "id": "AUieDaZITeZtLax8q2qv-F2M5jbZGQQ9xhpxuvM915c9lZqG",
                "language": "en-US",
                "auto_generated": False,
            },
        ]
    ).returning(Caption)

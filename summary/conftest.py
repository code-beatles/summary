from __future__ import annotations

import logging
from pathlib import Path

import pytest
from ujson import load

logger = logging.getLogger("tests")
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler())

FIXTURES = Path(__file__).parent / "utils" / "conftest" / "fixtures"


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
def fixtures():
    def load_fixture(name, *, json=True):
        with (FIXTURES / name).open() as f:
            if json:
                return load(f)
            return f.read()

    return load_fixture


@pytest.fixture()
async def video():
    from summary.models import Video

    return await Video.create(id="gqaHkPEZAew")


@pytest.fixture()
async def captions(video, fixtures):
    from summary.models import Caption

    data = fixtures("captions.json")

    return await Caption.insert_many(
        [
            {
                "video": video,
                "language": item["language"],
                "auto_generated": item["auto_generated"],
                "url": item["url"],
            }
            for item in data
        ]
    ).returning(Caption)


@pytest.fixture()
async def caption(fixtures, captions):
    data = fixtures("caption-data.json")
    caption = captions[1]
    caption.data = data
    return await caption.save()

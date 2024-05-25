from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from summary.models import Video


async def get_captions(video: Video) -> None:
    pass

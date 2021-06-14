import logging

import fastapi
from fastapi import Header, status
from fastapi.requests import Request
from fastapi.responses import Response
from fastapi.templating import Jinja2Templates

# from fastapi.responses import StreamingResponse
from netflix_mock.settings import Settings

logger = logging.getLogger(__name__)

router = fastapi.APIRouter()

settings = Settings()

templates = Jinja2Templates(directory=str(settings.server.template.dir))


@router.get("/video")
async def read_root(request: Request):
    return templates.TemplateResponse(
        "video.html",
        context={"request": request},
    )


# @router.get("/video/play")
# def play():
#     # use normal 'def' because standard open() that doesn't support async and await
#     stream = open(video_path, mode="rb")
#     return StreamingResponse(stream, media_type="video/mp4")


# -- HTTP range requests: https://developer.mozilla.org/en-US/docs/Web/HTTP/Range_requests


@router.get("/video/play")
async def play(file: str, range_: str = Header(alias="range", default=None)):
    range_ = range_.replace("bytes=", "")
    start, end = range_.split("-")
    start = int(start)
    end = int(end) if end else start + settings.server.video.chunk_size
    video_path = settings.server.video.dir / file
    filesize = video_path.stat().st_size
    with open(video_path, "rb") as stream:
        stream.seek(start)
        data = stream.read(end - start)
        length = len(data)
        content_range = f"bytes {start}-{start+length-1}/{filesize}"
        logger.info(f"Content-Range: {content_range}")
        return Response(
            status_code=status.HTTP_206_PARTIAL_CONTENT,
            content=data,
            headers={
                "Content-Range": content_range,
                "Content-Length": str(length),
                "Accept-Ranges": "bytes",
            },
            media_type="video/mp4",
        )

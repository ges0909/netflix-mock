import logging
from typing import Generator

import cv2
import fastapi
from fastapi import Header, status
from fastapi.requests import Request
from fastapi.responses import Response, StreamingResponse
from fastapi.templating import Jinja2Templates

from netflix_mock.settings import Settings

logger = logging.getLogger(__name__)

settings = Settings()

templates = Jinja2Templates(directory=str(settings.server.template.dir))

router = fastapi.APIRouter()


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


def _generate_frames() -> Generator[str, None, None]:
    camera = cv2.VideoCapture(0)  # local camera
    while True:
        success, frame = camera.read()  # read camera frame
        if success:
            _, buffer = cv2.imencode(".jpg", frame)
            frame_ = buffer.tobytes()
            # concat frame one by one and show result
            yield b"--frame\r\n" b"Content-Type: image/jpeg\r\n\r\n" + frame_ + b"\r\n"
        else:
            break


@router.get("/camera_feed")
async def camera_feed():
    return StreamingResponse(
        _generate_frames(),
        media_type="multipart/x-mixed-replace;boundary=frame",
    )

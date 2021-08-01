import logging
from typing import Generator

import cv2
import fastapi
from fastapi import Header, HTTPException, status
from fastapi.responses import Response, StreamingResponse

from netflix_mock.settings import get_settings

logger = logging.getLogger(__name__)

settings = get_settings()

router = fastapi.APIRouter()


# @router.get("/video/play")
# def play():
#     # use normal 'def' because standard open() that doesn't support async and await
#     stream = open(video_path, mode="rb")
#     return StreamingResponse(stream, media_type="video/mp4")


# -- HTTP range requests: https://developer.mozilla.org/en-US/docs/Web/HTTP/Range_requests


@router.get("/play")
async def play(file: str, range_: str = Header(alias="range", default=None)):
    range_ = range_.replace("bytes=", "")
    start, end = range_.split("-")
    start = int(start)
    end = int(end) if end else start + settings.server.video.chunk_size
    video_path = settings.server.video.dir / file
    file_size = video_path.stat().st_size
    with open(video_path, "rb") as stream:
        stream.seek(start)
        data = stream.read(end - start)
        length = len(data)
        content_range = f"bytes {start}-{start+length-1}/{file_size}"
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


@router.get("/capture")
async def capture():
    def _generate_frames() -> Generator[str, None, None]:
        capture_ = cv2.VideoCapture(0)  # local camera
        if not capture_.isOpened():
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="init video capture failed",
            )
        while True:
            success, image = capture_.read()  # read camera frame
            if not success:
                break
            success, buffer = cv2.imencode(ext=".jpg", img=image)
            if not success:
                break
            frame = buffer.tobytes()
            yield b"--frame\r\n" b"Content-Type: image/jpeg\r\n\r\n" + frame + b"\r\n"
        capture_.release()

    return StreamingResponse(
        _generate_frames(),  # concat frame one by one and show result
        media_type="multipart/x-mixed-replace;boundary=frame",
    )

import logging
from pathlib import Path

import fastapi
from fastapi import Header, status
from fastapi.requests import Request
from fastapi.responses import Response
from fastapi.templating import Jinja2Templates

logger = logging.getLogger(__name__)

router = fastapi.APIRouter()


templates_dir = Path(__file__).parent / ".." / "templates"
templates = Jinja2Templates(directory=str(templates_dir))

videos_dir = Path(__file__).parent / ".." / "videos"
video_path = videos_dir / "sample.mp4"

CHUNK_SIZE = 1024 * 1024


@router.get("/video")
async def read_root(request: Request):
    return templates.TemplateResponse(
        "video.html",
        context={"request": request},
    )


@router.get("/video/play")
async def video_endpoint(range: str = Header(None)):
    start, end = range.replace("bytes=", "").split("-")
    start = int(start)
    end = int(end) if end else start + CHUNK_SIZE
    filesize = video_path.stat().st_size
    logger.info(f"play video: chunk requested, range {start}-{end}")
    with open(video_path, "rb") as stream:
        stream.seek(start)
        data = stream.read(end - start)
        headers = {
            "Content-Range": f"bytes {str(start)}-{str(end)}/{filesize}",
            "Accept-Ranges": "bytes",
        }
        logger.info(f"play video: chunk returned, range {start}-{end}, filesize {filesize}")
        return Response(
            data,
            status_code=status.HTTP_206_PARTIAL_CONTENT,
            headers=headers,
            media_type="video/mp4",
        )

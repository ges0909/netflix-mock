import logging
import wave

import fastapi
import pyaudio
from fastapi.responses import StreamingResponse

from netflix_mock.settings import get_settings

logger = logging.getLogger(__name__)

router = fastapi.APIRouter()

settings = get_settings()


@router.get("/play")
def play(file: str):
    # use normal 'def' because standard open() that doesn't support async and await
    audio_path = settings.server.audio.dir / file
    stream = open(audio_path, mode="rb")
    return StreamingResponse(stream, media_type="audio/mpeg")


@router.get("/record")
def record():
    chunk = settings.server.audio.chunk_size  # Record in chunks of 1024 samples
    sample_format = pyaudio.paInt16  # 16 bits per sample
    channels = 2
    fs = 44100  # Record at 44100 samples per second
    seconds = 3
    filename = "output.wav"

    p = pyaudio.PyAudio()  # Create an interface to PortAudio

    logger.info("start audio recording ...")

    stream = p.open(format=sample_format, channels=channels, rate=fs, frames_per_buffer=chunk, input=True)

    frames = []  # initialize array to store frames

    # store data in chunks for 3 seconds
    for i in range(0, int(fs / chunk * seconds)):
        data = stream.read(chunk)
        frames.append(data)

    # stop and close the stream
    stream.stop_stream()
    stream.close()

    # terminate the PortAudio interface
    p.terminate()

    logger.info("stop audio recording")

    # save the recorded data as a WAV file
    wf = wave.open(filename, "wb")
    wf.setnchannels(channels)
    wf.setsampwidth(p.get_sample_size(sample_format))
    wf.setframerate(fs)
    wf.writeframes(b"".join(frames))
    wf.close()

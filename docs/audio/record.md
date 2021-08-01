# Audio recording

[Record](/audio/record)

## Install PyAudio

- download wheel (e.g. `PyAudio-0.2.11-cp39-cp39-win_amd64.whl`) from [Unofficial Windows Binaries for Python Extension Packages](https://www.lfd.uci.edu/~gohlke/pythonlibs/)
- add to `pyproject.toml`
  ```toml
  [tool.poetry.dependencies]
  pyaudio = { file = "wheels/PyAudio-0.2.11-cp39-cp39-win_amd64.whl" }
  ```
- `poetry install`

## Related

- [Playing and Recording Sound in Python](https://realpython.com/playing-and-recording-sound-python/)
- [High Quality Audio with Python and PyAudio](https://dolby.io/blog/capturing-high-quality-audio-with-python-and-pyaudio)

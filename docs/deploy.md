# Deploy to Production

## On local (WSL2)

1. export without _dev_ dependencies: `poetry export -f requirements.txt -o requirements.txt --without-hashes`
1. `pip wheel --no-binary :all: --wheel-dir wheelhouse -r requirements.txt`
1. update doc: `poetry run mkdocs build`
1. create app wheel (doc's included): `poetry build`
1. copy app wheel to other wheels: `cp dist/netflix_mock-0.1.0-py3-none-any.whl wheelhouse`
1. `tar -cvzf netflix-mock.tar wheelhouse/`

- `pip download --only-binary :all: --dest wheelhouse --platform linux_x86_64 --python-version 3.6.8 --implementation cp -r requirements.txt `

## On remote (Linux)

1. create installation dir: `mkdir netflix-mock && cd netflix-mock`
1. `tar -xvzf netflix-mock.tar.gz`
1. create venv: `python3 -m venv venv`
1. activate venv: `. venv/bin/activate`
1. `pip install wheelhouse/*`

## Create a _Systemd_ service

```ini
[Unit]
Description=<project description>

[Service]
User=<user e.g. root>
WorkingDirectory=<path to your project directory>
Environment="PATH=<path to virtual environment>/bin"
ExecStart=<path to python script>

[Install]
WantedBy=multi-user.target
```

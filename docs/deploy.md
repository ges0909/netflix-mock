# Deploy

On local (WSL2):

1. `poetry export -f requirements.txt -o requirements.txt --without-hashes`
1. `pip wheel --no-binary :all: --wheel-dir wheelhouse -r requirements.txt`
1. `poetry build`
1. `cp dist/netflix_mock-0.1.0-py3-none-any.whl wheelhouse`
1. `tar cf netflix-mock.tar wheelhouse/`
1. `gzip netflix-mock.tar`

On remote (Linux):

1. create installation dir: `mkdir netflix-mock && cd netflix-mock`
1. `gzip -d netflix-mock.tar.gz`
1. `tar xf netflix-mock.tar`
1. create venv: `python3 -m venv venv`
1. activate venv: `. venv/bin/activate`
1. `pip install wheelhouse/*`

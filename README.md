# Netflix Mock

## Install

```sh
git clone git@github.com:ges0909/netflix-mock.git
poetry cd netflix-mock
poetry install
poetry run pre-commit install
```

## MkDocs

```sh
poetry run mkdocs build
```

## Run

```sh
uvicorn main:app --reload
```

## Pre-commit Hooks

```sh
poetry run pre-commit run --all-files
```

## Coverage

```shell
pytest --cov netflix_mock .
coverage html
start htmlcov/index.html
```

## Schemathesis

Property Based Testing (PBT)

```sh
poetry run schemathesis run --checks all http://localhost:8000/api/openapi.json
poetry run schemathesis run --method GET http://localhost:8000/api/openapi.json
poetry run schemathesis run --endpoint /api http://localhost:8000/api/openapi.json
```

## Deploy to Prod

On local (WSL2):

1. export without _dev_ dependencies: `poetry export -f requirements.txt -o requirements.txt --without-hashes`
1. `pip wheel --no-binary :all: --wheel-dir wheelhouse -r requirements.txt`
1. update doc: `poetry run mkdocs build`
1. create app wheel (doc's included): `poetry build`
1. copy app wheel to other wheels: `cp dist/netflix_mock-0.1.0-py3-none-any.whl wheelhouse`
1. `tar -cvzf netflix-mock.tar wheelhouse/`

<!--
`pip download --only-binary :all: --dest wheelhouse --platform linux_x86_64 --python-version 3.6.8 --implementation cp -r requirements.txt `
-->

On remote (Linux):

1. create installation dir: `mkdir netflix-mock && cd netflix-mock`
1. `tar -xvzf netflix-mock.tar.gz`
1. create venv: `python3 -m venv venv`
1. activate venv: `. venv/bin/activate`
1. `pip install wheelhouse/*`

Create a _Systemd_ service:

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

## Install CentOS on WSL 2

- [How to install CentOS 8 on WSL 1 or 2 of Windows 10](https://www.how2shout.com/how-to/how-to-install-centos-8-on-wsl-windows-10.html)
- [Configure an interpreter using WSL](https://www.jetbrains.com/help/pycharm/using-wsl-as-a-remote-interpreter.html) (requires _PyCharm Professional_)

Windows:

- prerequisite: WSL is **enabled**
- download CentOS\*.zip from [CentOS-WSL](https://github.com/mishamosher/CentOS-WSL)
- unzip CentOS\*.zip
- execute CentOS\*.exe
- execute CentOS\*.exe again; issue `dnf update`
- show installed distros: `wsl --list --verbose`
- remove distro: `./CentOS8.exe clean` (as _Admin_) or `wsl --unregister CentOS8`

CentOS:

```sh
yum -y install python3 python3-wheel git gcc gcc-c++ python3-devel
useradd develop
passwd develop
su - develop
```

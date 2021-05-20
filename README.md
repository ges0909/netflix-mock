# README

## Read

- [Let's Build a Fast, Modern Python API with FastAPI](https://www.youtube.com/watch?v=sBVb4IB3O_U)
- [FastAPI logging](https://philstories.medium.com/fastapi-logging-f6237b84ea64)
- [Deploy to Production](https://flask.palletsprojects.com/en/latest/tutorial/deploy/)
- [How to create a Systemd service in Linux](https://www.shubhamdipt.com/blog/how-to-create-a-systemd-service-in-linux/)

## Setup

```sh
poetry new netflix-mock && cd netflix-mock
poetry add fastapi typer pydantic python-dotenv sqlalchemy httpx jinja2 aiofiles uvicorn python-multipart
poetry add -D black requests requests-toolbelt mkdocs mkdocs-material
```

## Run

```sh
uvicorn main:app --reload
```

## MkDocs

Generate static HTML site from Markdown.

```sh
poetry run mkdocs new .
poetry run mkdocs build
```

## Deploy to production

On local (Windows):

1. `poetry shell`
1. `pip wheel --no-binary :all: -w wheelhouse fastapi httpx SQLAlchemy typer aiofiles Jinja2 uvicorn async-exit-stack async_generator python-multipart python-dotenv`
1. `exit`
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

## Install CentOS on WSL 2

- [How to install CentOS 8 on WSL 1 or 2 of Windows 10](https://www.how2shout.com/how-to/how-to-install-centos-8-on-wsl-windows-10.html)
- [Configure an interpreter using WSL](https://www.jetbrains.com/help/pycharm/using-wsl-as-a-remote-interpreter.html) (requires _PyCharm Professional_)

Windows:

- prerequisite: WSL is **enabled**
- download CentOS*.zip from [CentOS-WSL](https://github.com/mishamosher/CentOS-WSL)
- unzip CentOS*.zip
- execute CentOS*.exe
- execute CentOS*.exe again; issue `dnf update`
- show installed distros: `wsl --list --verbose`
- remove distro: `./CentOS8.exe clean` (as _Admin_) or `wsl --unregister CentOS8`

CentOS:

```sh
yum -y install python3 python3-wheel git gcc gcc-c++ python3-devel
useradd develop
passwd develop
su - develop
```

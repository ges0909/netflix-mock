# README

## Read

- [Let's Build a Fast, Modern Python API with FastAPI](https://www.youtube.com/watch?v=sBVb4IB3O_U)
- [FastAPI logging](https://philstories.medium.com/fastapi-logging-f6237b84ea64)
- [Deploy to Production](https://flask.palletsprojects.com/en/latest/tutorial/deploy/)

## Setup

```sh
poetry new netflix-mock && cd netflix-mock
poetry add fastapi typer pydantic pydantic[dotenv] sqlalchemy httpx jinja2 aiofiles uvicorn
poetry add -D black requests mkdocs mkdocs-material
```

## Run

```sh
uvicorn main:app --reload
```

## Mkdocs

Generate static HTML site from Markdown.

```sh
poetry run mkdocs new .
poetry run mkdocs build
```

## Deploy to production

On local (Windows):

1. create a wheel: `python setup.py bdist_wheel` (requires `setup.py`) or `poetry build`
1. copy files to remote, e.g. dist/netflix-mock-0.1.0-py3-none-any.whl, dev.env, logging.conf

On remote (Linux):

1. create installation dir: `mkdir netflix-mock && cd netflix-mock`
1. create venv: `python3 -m venv venv`
1. activate venv: `. venv/bin/activate`
1. install: `pip3 install netflix-mock-0.1.0-py3-none-any.whl`
1. run: `python3 -m netflix-mock.main --env dev.env --log logging.conf`

## Install CentOS on WSL 2

- [How to install CentOS 8 on WSL 1 or 2 of Windows 10](https://www.how2shout.com/how-to/how-to-install-centos-8-on-wsl-windows-10.html)
- [Configure an interpreter using WSL](https://www.jetbrains.com/help/pycharm/using-wsl-as-a-remote-interpreter.html) (requires _PyCharm Professional_)

Windows:

- prerequisite: WSL is **enabled**
- download CentOS 8 WSL files from [CentWSL](https://github.com/wsldl-pg/CentWSL/releases)
- unzip CentOS8.zip
- execute CentOS8.exe
- execute CentOS8.exe again; issue `dnf update`
- show installed distros: `wsl --list --verbose`
- remove distro: `./CentOS8.exe clean` (as _Admin_) or `wsl --unregister CentOS8`

CentOS:

```sh
sudo yum install python3 python3-wheel
python3 --version
pip3 --version
```

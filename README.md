# README

- [Let's Build a Fast, Modern Python API with FastAPI](https://www.youtube.com/watch?v=sBVb4IB3O_U)
- [FastAPI logging](https://philstories.medium.com/fastapi-logging-f6237b84ea64)

## CentOS on WSL 2

- [How to install CentOS 8 on WSL 1 or 2 of Windows 10](https://www.how2shout.com/how-to/how-to-install-centos-8-on-wsl-windows-10.html)
- [Configure an interpreter using WSL](https://www.jetbrains.com/help/pycharm/using-wsl-as-a-remote-interpreter.html) (requires _PyCharm Professional_)

Windows: 

- prerequisite: WSL is **enabled**
- download CentOS 8 WSL files from [CentWSL](https://github.com/wsldl-pg/CentWSL/releases)
- unzip _CentOS8.zip_
- execute _CentOS8.exe_
- execute _CentOS8.exe_ again; issue `dnf update`
- show installed distros: `wsl --list --verbose`
- remove distro:
  - `./CentOS8.exe clean` (as _Admin_)
  - or
  - `wsl --unregister <distro>`

Cent OS:

```sh
sudo yum install python3 python3-wheel
python3 --version
pip3 --version
```

## Setup project

```sh
poetry new netflix-mock && cd netflix-mock
poetry add fastapi typer pydantic pydantic[dotenv] sqlalchemy httpx jinja2
```

```sh
poetry add -D black uvicorn
```

### MkDocs

```sh
poetry add aiofiles
poetry add -D mkdocs mkdocs-material
poetry run mkdocs new .
poetry run mkdocs build
```

## Run locally

```sh
uvicorn main:app --reload
```

## Deploy

1. create distribution: `poetry update`
1. copy files _dist/mock_server-0.1.0-py3-none-any.whl_, _dev.env_ and _logging.conf_ to remote
   
On remote:

1. create venv: `python3 -m venv venv`
1. activate venv: `source venv/bin/activate`
1. install: `pip3 install mock_server-0.1.0-py3-none-any.whl`
1. run: `python3 -m mock.main --env dev.env --log logging.conf`

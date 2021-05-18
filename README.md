# README

- [Let's Build a Fast, Modern Python API with FastAPI](https://www.youtube.com/watch?v=sBVb4IB3O_U)
- [FastAPI logging](https://philstories.medium.com/fastapi-logging-f6237b84ea64)

## CentOS on WSL 2

- [How to install CentOS 8 on WSL 1 or 2 of Windows 10](https://www.how2shout.com/how-to/how-to-install-centos-8-on-wsl-windows-10.html)
- [Configure an interpreter using WSL](https://www.jetbrains.com/help/pycharm/using-wsl-as-a-remote-interpreter.html), requires _PyCharm Professional_
- [How to package a python project with all of its dependencies for offline install](https://medium.com/@amimahloof/how-to-package-a-python-project-with-all-of-its-dependencies-for-offline-install-7eb240b27418)

Windows: 

- prerequiste: WSL is **enabled**
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

## Setup

```sh
poetry new mock-server && cd mock-server
poetry add fastapi typer pydantic pydantic[dotenv] sqlalchemy jinja2 httpx jsf
```

```sh
poetry add -D black
poetry add -D uvicorn
```

## MkDocs

Serve static files:

```sh
poetry add aiofiles
poetry add -D mkdocs mkdocs-material
poetry run mkdocs new .
poetry run mkdocs build
```

## Run

```sh
uvicorn main:app --reload
```

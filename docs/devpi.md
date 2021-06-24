# DevPi

# Create virtual env

```shell
python -m venv venv
venv\Script\activate
```

## Install

```shell
(venv) pip install devpi-server
(venv) devp-server --version
```

## Init

```shell
(venv) devpi-init
```

## Create config file

```shell
(venv) devpi-gen-config
```

## Run in background (only nix systems)

```shell
pip install supervisor
```

## Related

- [Manage your Python Packages Workflow](https://www.devpi.net/)
- [devpi: PyPI server and packaging/testing/release tool](https://devpi.net/docs/devpi/devpi/stable/%2Bd/index.html)

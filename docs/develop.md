# Develop

Install:

```sh
poetry add -D poetry-githooks
```

Configure _pyproject.toml_:

```toml
[tool.githooks]
pre-commit = [
    "poetry -f requirements.txt -o requirements.txt --without-hashes",
    "mkdocs build"
]
```

Setup newly added githooks:

```sh
poetry run githooks setup
```

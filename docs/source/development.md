# Development

## Setting up Virtual Environment

install virtualenv

```
pip install --upgrade virtualenv
```

create virtual environment

```
virtualenv venv
```

venv activation (windows)

```
source venv/Scripts/activate
```

install dev-requirements

```
pip install -r dev-requirements.txt
```

venv deactivation

```
deactivate
```

generate new requirements.txt

```
pip freeze > requirements.txt
```

## Build Package

```
pip install --upgrade build

python -m build
```

## Publish to PyPi

```
pip install --upgrade twine

python -m twine upload dist/*
```

## Sphinx Docs Build

```
pip install --upgrade sphinx

sphinx-build docs/source docs/build
```

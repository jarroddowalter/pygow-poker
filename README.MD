# pygow-poker

Simulate or play your favorite pai gow poker variant with python!

## Installation

Run the following to install

```
pip install pygow-poker
```

On init (Windows)

```
python -m virtualenv venv

source venv/Scripts/activate

pip install -r dev-requirements.txt
```

On init (Mac)

```
virtualenv venv

source venv/bin/activate

pip install -r dev-requirements.txt
```

Build

```
pip install --upgrade build

python -m build
```

Publish

```
pip install --upgrade twine

python -m twine upload dist/*
```

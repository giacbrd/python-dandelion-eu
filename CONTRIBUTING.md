# Contributing

## Getting started with development

### Setup

There are several ways to create your isolated environment. This is the default method.

Run the following in a terminal:

```
# Clone the repository
git clone https://github.com/giacbrd/python-dandelion-eu.git

# Enter the repository
cd python-dandelion-eu

# Create then activate a virtual environment
python -m venv venv
source venv/bin/activate

# Install the development requirements
python -m pip install -r requirements/dev.txt
```

### Run tests

Once setup, you should be able to run tests:
```
pytest
```

## Install Pre-commit Hooks


Pre-commit hooks are scripts that run every time you make a commit. If any of the scripts fail, it stops the commit. You can see a listing of the checks in the ``.pre-commit-config.yaml`` file.

```
pre-commit install
```

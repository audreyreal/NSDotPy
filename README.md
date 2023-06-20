# NSDotPy

A Python wrapper around httpx for legally interacting with the HTML NationStates site, as well as a barebones API client. Built for legality first and foremost, as well as ease of use.

## Installation

`pip install nsdotpy`

## Simple Example

```python

from nsdotpy.session import NSSession
session = NSSession("NSDotPy Example", "1.0.0", "Script Author's nation", "Script User's nation")

if session.login("User Nation", "Password"):  # logs in and checks if login was successful
    session.move_to_region("Lily")  # only moves if you successfully logged in

# an API client is also available, here's a simple example
data = session.api_request("world", shard="nations")
# it returns a benedict object (https://github.com/fabiocaccamo/python-benedict), which is a dict with some extra features
# you can access the data like a normal dict
nations = data["nations"].split(",")
# or you can use a keyattribute (my personal favorite)
nations = data.nations.split(",")
```

## TODO:

- ~~Region Admin Controls~~
- Dossier and reports handling
- More fleshed out API Client
- ~~Cards support~~ Shoutouts to 9003
- ~~Migrate automatic docs generation, code formatting, and PyPI uploading to GitHub Actions for better CI~~

## Docs

https://audreyreal.github.io/NSDotPy/nsdotpy/session.html#NSSession

## Generating Docs

1. [Ensure poetry is installed](https://python-poetry.org/docs/#installation), or your system's package manager if applicable.
2. Run `poetry install` in the root directory of the project to install dependencies if you haven't already.
3. Run `poetry run pdoc nsdotpy/session.py -d=google -o=docs/` to generate the docs

## Publishing to PyPi (for maintainers)

1. [Ensure poetry is installed](https://python-poetry.org/docs/#installation), or your system's package manager if applicable.
2. Run `poetry install` in the root directory of the project to install dependencies if you haven't already.
3. Run `poetry build` to build the package. Ensure the version number in `pyproject.toml` is correct against the version number in `session.py`.
4. Run `poetry publish` to publish the package to PyPi. You will need to have a PyPi account have supplied your API key to poetry.

## Contributing

Pull requests are welcome. Ensure all code is formatted with `black`, that functions are type annotated (type annotating function variables not necessary), and docstrings are present using the Google style. If you use VSCode, [you can use this extension for easy docstring generation.](https://marketplace.visualstudio.com/items?itemName=njpwerner.autodocstring)

## License

[AGPL3.0-or-later](https://choosealicense.com/licenses/agpl-3.0/). Any project that uses this library must be licensed under AGPL3.0-or-later as well. If being used in a web application, the source code must be prominently made available to users.

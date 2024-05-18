# alogamous

[![PyPI - Version](https://img.shields.io/pypi/v/alogamous.svg)](https://pypi.org/project/alogamous)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/alogamous.svg)](https://pypi.org/project/alogamous)

-----

## Table of Contents

- [Installation](#installation)
- [License](#license)

## Installation

```console
pip install alogamous
```

## Development

1. Open a terminal

1. Install [hatch](https://hatch.pypa.io/latest/)

    ```bash
    curl -Lo hatch-universal.pkg https://github.com/pypa/hatch/releases/latest/download/hatch-universal.pkg
    sudo installer -pkg ./hatch-universal.pkg -target /
    ```

1. Restart your terminal

    Hatch modifies your system PATH variable, and this won't take effect unless you restart the terminal.

1. Make sure hatch works

    ```bash
    hatch --version
    ```

1. Clone the repo

    ```bash
    git clone https://github.com/aquanauts/alogamous.git
    cd alogamous
    ```

1. Install pre-commit hooks

    This will make sure certain checks are run when committing code.

    ```bash
    hatch run pre-commit:install
    ```

1. Run the tests

    ```bash
    hatch test
    ```

1. Setup your IDE

    ???

## License

`alogamous` is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.

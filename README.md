# Alogamous

[![PyPI - Version](https://img.shields.io/pypi/v/alogamous.svg)](https://pypi.org/project/alogamous)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/alogamous.svg)](https://pypi.org/project/alogamous)

-----

## Table of Contents

- [Description](#description)
- [Installation](#installation)
- [Development](#development)
- [License](#license)

## Description
A Python program that can process log files and generate a daily report on anomalies in a set of logs.
- It should be able to read multiple files and output an html-formatted file.
- It should have multiple metrics/checks for anomalous log lines.
- It should be able to take in a log line format so that it knows how to extract useful information from a log line.
- It should be able to traverse a well-defined file system structure to access all logs.
- It should be able to generate metrics that span multiple files.
- It should be well-tested.


## Installation

```console
pip install alogamous
```

## Development

### Setup
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

1. Configure hatch

    ```bash
    hatch config set dirs.env.virtual .venv
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

   1. Sign up for a free [JetBrains Educational License](https://www.jetbrains.com/community/education/#students) or buy one

   2. Download [Pycharm](https://www.jetbrains.com/pycharm/download/)
      - Depending on your platform you may need to download and install [Python](https://www.python.org/)

   3. Open Pycharm

   4. Click Open on the welcome screen and then select the file alogamous



### Possible Errors

**Permission Error**

   - Message: *PermissionError: [Errno 13] Permission denied: '/usr/local/hatch/bin/hatch'*

   - Fix by running:
      ```bash
      sudo chmod a+r /usr/local/hatch/bin/hatch
      ```
### Adding to Gitignore
Gitignore is a way to explicitly tell Git that certain files should not be committed.
For example, we did this with the .idea folder, which is automatically generated and contains settings that do not need to be committed.
- Create the gitignore file
   ```bash
  touch .gitignore
- Add the current file to the gitignore
   ```bash
   git add .
- Add the present file to the gitignore
   ```bash
   git commit

## License

`alogamous` is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.

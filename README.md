# pronote-tools
Additional tools for PRONOTE

## Description
`pronote-tools` is a project based on the `pronotepy` library. Its goal is to give better interface and functionnalities to PRONOTE for the users, like **Python console prompt** or **mobile notifications**.

## Table of Contents
- [Requirements](#requirements)
- [Installation](#installation)

## Requirements
To run most programs of this project, you'll need to install **Python** (Python3).
There are **.sh** files that can help you for a better installation. Follow carefully the instructions for your OS.

## Installation and basic usage
Follow these steps to set up the project:

1. Clone the repository:
    ```shell
    git clone https://github.com/leoo84/pronote-tools.git
    cd pronote-tools
    ```

2. Install dependencies and run a script:
    If you are on **Linux**, you can run the `start-linux.sh` file. It will automatically do all the work, you have just to enter the name of the python file you want to execute.
    ```shell
    # run start-py.sh
    ./start-linux.sh
    ```
    If you are on **Windows**, you can run the `setup-windows.py` file.
    ```shell
    # run setup-windows.py
    python3 setup-windows.py
    ```

    If you are on another operating system, you have to manually install dependencies and run the script you want.
    ```shell
    # install dependencies
    pip install -q pycryptodome beautifulsoup4 requests autoslot tabulate pronotepy openpyxl pandas fpdf xlsxwriter

    # run a script
    python [your-python-file]
    ```
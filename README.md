![Static Badge](https://img.shields.io/badge/python-3.10-%233776AB?logo=python)
![Static Badge](https://img.shields.io/badge/Beautiful%20Soup%204-v4.12.3-%233776AB)


# bs4 parser

A small pep entries parser based on Beautiful Soup 4 library

## Table of Contents
- [Installation](#installation)
- [Usage](#usage)
- [Author](#author)

## Installation

### basic
1. Clone the repository:

    ```bash
    git clone https://github.com/alisher-nil/bs4_parser.git
    ```

2. Navigate to the project directory:

    ```bash
    cd bs4_parser
    ```

3. Install the required dependencies:

    ```bash
    pip install -r requirements.txt
    ```
### uv
Requires [uv](https://docs.astral.sh/uv/) package manager.
1. Clone the repository:

    ```bash
    git clone https://github.com/alisher-nil/bs4_parser.git
    ```

2. Navigate to the project directory:

    ```bash
    cd bs4_parser
    ```

3. Install the required dependencies:

    ```bash
    uv sync
    ```

## Usage

To run the PEP parser, use the following command from the project directory:

```bash
python main.py {whats-new,latest-versions,download} [-h] [-c] [-o {pretty,file}] 
# or with uv
uv run main.py {whats-new,latest-versions,download} [-h] [-c] [-o {pretty,file}] 
```

## Author
Please feel free to contact me with any questions or feedback:

- Email: alisher.nil@gmail.com
- GitHub: [alisher-nil](https://github.com/alisher-nil/)
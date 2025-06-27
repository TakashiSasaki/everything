# Everything CLI Tools

This project provides command-line interface (CLI) tools to interact with the Everything search engine, leveraging its DLL, `es.exe` (command-line utility), and HTTP API.

## Features

- **`everything-dll`**: Interact with Everything via its DLL for fast, direct searches.
- **`everything-es`**: Utilize the `es.exe` command-line tool for searches.
- **`everything-http`**: Connect to the Everything HTTP server for remote or local searches.
- **Flexible Output**: Get search results in plain text or JSON format.
- **Test Mode**: Built-in connectivity tests for each method.

## Requirements

- **Everything Search Engine**: You need to have the Everything search engine installed on your Windows machine.
- **`es.exe`**: For `everything-es`, ensure `es.exe` is in your system's PATH or in the project directory.
- **Everything DLL**: For `everything-dll`, ensure `Everything64.dll` (for 64-bit Python) or `Everything32.dll` (for 32-bit Python) is in your system's PATH or in the project directory.
- **Everything HTTP Server**: For `everything-http`, the Everything HTTP server must be running and accessible.

## Installation

This project uses [Poetry](https://python-poetry.org/) for dependency management. If you don't have Poetry installed, follow their official installation guide.

1. **Clone the repository (if you haven't already):**
   ```bash
   git clone https://github.com/your-username/everything-cli.git
   cd everything-cli
   ```

2. **Install dependencies using Poetry:**
   ```bash
   poetry install
   ```

3. **(Optional) Activate the virtual environment:**
   ```bash
   poetry shell
   ```
   You can also run commands directly using `poetry run <command>`. For example, `poetry run everything-dll --help`.

## Usage

Each tool can be run using `poetry run <tool-name>`. Use the `--help` flag for detailed options.

### `everything-dll`

Interacts directly with the Everything DLL.

```bash
poetry run everything-dll --help
poetry run everything-dll --search "your query" --json
poetry run everything-dll --test
```

### `everything-es`

Uses the `es.exe` command-line utility.

```bash
poetry run everything-es --help
poetry run everything-es --search "your query" --all-fields
poetry run everything-es --test
```

### `everything-http`

Connects to the Everything HTTP server. Ensure the server is running.

```bash
poetry run everything-http --help
poetry run everything-http --search "your query" --host 127.0.0.1 --port 8080 --json
poetry run everything-http --test
```

### Environment Variables (for `everything-http`)

You can configure the HTTP host and port using a `.env` file in the project root:

```
EVERYTHING_HOST=127.0.0.1
EVERYTHING_PORT=80
```

## Running Tests

To run the unit tests for the project:

```bash
poetry run python -m pytest test/
```

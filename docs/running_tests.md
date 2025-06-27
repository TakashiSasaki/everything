# Running the Test Suite

To run the test suite for this project, follow these steps:

1.  **Ensure Poetry is installed and configured.**
    If you haven't already, install Poetry by following the instructions on the official Poetry website: [https://python-poetry.org/docs/#installation](https://python-poetry.org/docs/#installation)

2.  **Install project dependencies.**
    Navigate to the root directory of the project in your terminal and install the dependencies using Poetry:
    ```bash
    poetry install
    ```

3.  **Run the tests.**
    Once the dependencies are installed, you can execute the test suite using the following command:
    ```bash
    python -m poetry run pytest
    ```

This command will discover and run all tests in the project, providing a summary of the results.

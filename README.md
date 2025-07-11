# LLM Code Evaluator

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/badge/python-3.9%2B-blue.svg)](https://www.python.org/downloads/)
[![Docker Support](https://img.shields.io/badge/docker-ready-blue.svg)](https://www.docker.com/)
[![Contributions Welcome](https://img.shields.io/badge/contributions-welcome-brightgreen.svg?style=flat)](./CONTRIBUTING.md)

An advanced, command-line tool for evaluating the performance of Large Language Models (LLMs) on coding problems. This framework systematically tests model-generated code against a predefined set of challenges, providing detailed metrics on correctness, performance, and other key characteristics.

![Demo Screenshot](https://i.imgur.com/example-image.png)  <!-- It's highly recommended to replace this with an actual screenshot of your tool in action -->

## Table of Contents

- [Features](#features)
- [How It Works](#how-it-works)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Local Installation](#local-installation)
- [Running with Docker](#running-with-docker)
  - [Docker Prerequisites](#docker-prerequisites)
  - [Build and Run](#build-and-run)
- [Usage](#usage)
- [File Descriptions](#file-descriptions)
- [Output](#output)
- [Contributing](#contributing)
- [License](#license)

## Features

*   **Model Agnostic:** Test any model available through the Ollama interface.
*   **Flexible Evaluation:** Run evaluations on all problems, or select specific ones on-the-fly.
*   **Rich Metrics:** Gathers data on correctness (pass/fail), execution time, code length, token counts, and generation time.
*   **Customizable Prompts:** Tailor output styles to test a model's instruction-following capabilities.
*   **Detailed Logging:** Saves comprehensive session logs and summary reports (`.csv`) for later analysis.
*   **Interactive Interface:** A user-friendly command-line menu for easy operation.
*   **Dockerized:** Run the evaluator in a containerized environment without managing local Python dependencies.
*   **Specialized Data Handling:** Includes helpers for complex data structures like binary trees as used in LeetCode problems.

## How It Works

The evaluation process follows these steps:

1.  **Problem Loading:** Loads coding challenges and test cases from `problems.json`.
2.  **Model & Style Selection:** The user interactively selects an LLM and a prompt output style.
3.  **Prompt Generation:** A detailed prompt is constructed using the problem description and the selected style template.
4.  **Code Generation:** The tool calls the Ollama API with the prompt to generate a code solution.
5.  **Code Extraction:** Python code is automatically parsed from the model's markdown response.
6.  **Execution & Validation:** The extracted code is executed in a safe environment against all predefined test cases.
7.  **Metric Collection:** Performance data from both generation and execution are logged.
8.  **Reporting:** Results are displayed in a summary table in the console and saved to detailed log files.

## Getting Started

### Prerequisites

*   [Ollama](https://ollama.ai/) installed and running on your host machine.
*   At least one model installed via Ollama (e.g., `ollama run llama3`).

### Local Installation

1.  **Clone the repository:**
    ```sh
    git clone https://github.com/your-username/llm-code-evaluator.git
    cd llm-code-evaluator
    ```

2.  **Create a virtual environment (recommended):**
    ```sh
    python3 -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3.  **Install the required Python packages:**
    ```sh
    pip install -r requirements.txt
    ```

## Running with Docker

Running the evaluator with Docker is the recommended method as it avoids the need to manage a local Python environment.

### Docker Prerequisites

*   [Docker](https://www.docker.com/products/docker-desktop/) installed and running.
*   Ollama must be running on your **host machine**. The container is configured to connect to it.

### Build and Run

1.  **Build the Docker image:**
    From the root of the project directory, run:
    ```sh
    docker build -t llm-evaluator .
    ```

2.  **Run the Docker container:**
    The `-it` flag is required to interact with the menu, and `--rm` cleans up the container after it exits. The command differs slightly based on your operating system.

    *   **On Windows or macOS (using Docker Desktop):**
        `host.docker.internal` is a special DNS name that allows the container to connect to the Ollama server on your host.
        ```sh
        docker run -it --rm llm-evaluator
        ```

    *   **On Linux:**
        You must use host networking and explicitly set the host variable.
        ```sh
        docker run -it --rm --network="host" -e OLLAMA_HOST="http://127.0.0.1:11434" llm-evaluator
        ```

    > **Note on Logs:** By default, log files are saved inside the container. To persist them on your host machine, mount a volume:
    > ```sh
    > # This command maps the 'logs' folder in your current directory to the '/app/logs' folder in the container.
    > docker run -it --rm -v "$(pwd)/logs:/app/logs" llm-evaluator
    > ```

## Usage

1.  **Ensure the Ollama service is running:**
    Open a terminal and run `ollama serve` if it's not already active.

2.  **Launch the application (either locally or via Docker):**
    ```sh
    # If running locally
    python dual_method_eval.py

    # Or if running with Docker
    docker run -it --rm llm-evaluator
    ```

3.  **Follow the interactive prompts:**
    *   Select the model you wish to evaluate.
    *   Choose a prompt/output style.
    *   Select an action: run all problems, pick a specific problem, change settings, or quit.

## File Descriptions

*   **`dual_method_eval.py`**: The main script that orchestrates the entire evaluation process.
*   **`helpers.py`**: Contains utility functions for handling complex data structures (e.g., building and parsing binary trees).
*   **`problems.json`**: A JSON file containing the coding problems, their prompts, and test cases. Easily extendable with new problems.
*   **`requirements.txt`**: A list of Python dependencies for the project.
*   **`Dockerfile`**: Defines the instructions to build the application's portable Docker image.
*   **`logs/`**: The directory where all session logs and reports are saved (created automatically).

## Output

The tool generates two primary forms of output for each session:

1.  **Console Report:** A summary table is printed to the console at the end of the session, showing key performance indicators for each test run.
2.  **Log Files:** For each session, two files are saved in the `logs/` directory, named with the session's timestamp:
    *   `sdk_session_log_... .txt`: A detailed text file containing full prompts and responses for debugging.
    *   `session_report_... .csv`: A structured CSV file containing all metrics, perfect for analysis in spreadsheets or data analysis tools.

## Contributing

Contributions are what make the open-source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

Please read `CONTRIBUTING.md` for details on our code of conduct and the process for submitting pull requests.

## License

Distributed under the MIT License. See `LICENSE.txt` for more information.

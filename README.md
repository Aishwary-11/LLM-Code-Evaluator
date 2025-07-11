# LLM Code Evaluator

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/badge/python-3.9%2B-blue.svg)](https://www.python.org/downloads/)
[![Contributions Welcome](https://img.shields.io/badge/contributions-welcome-brightgreen.svg?style=flat-square)](./CONTRIBUTING.md)

An advanced, command-line tool for evaluating the performance of Large Language Models (LLMs) on coding problems. This framework systematically tests model-generated code against a predefined set of challenges, providing detailed metrics on correctness, performance, and other key characteristics.

## Table of Contents

- [Features](#features)
- [How It Works](#how-it-works)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
- [Usage](#usage)
- [File Descriptions](#file-descriptions)
- [Output](#output)
- [Contributing](#contributing)

## Features

*   **Model Agnostic:** Test any model available through the Ollama interface.
*   **Flexible Evaluation:** Run evaluations on all problems, or select specific ones.
*   **Rich Metrics:** Gathers data on correctness, execution time, code length, token counts, and generation time.
*   **Customizable Prompts:** Tailor output styles to test model instruction-following capabilities.
*   **Detailed Logging:** Saves comprehensive session logs and summary reports for later analysis.
*   **Interactive Interface:** User-friendly command-line menus for easy operation.
*   **Specialized Data Handling:** Includes helpers for complex data structures like binary trees.

## How It Works

The evaluation process follows these steps:

1.  **Problem Loading:** Loads coding challenges from `problems.json`.
2.  **Model and Style Selection:** The user selects an LLM and an output style.
3.  **Prompt Generation:** A prompt is constructed using the problem description and the selected style.
4.  **Code Generation:** The tool calls the Ollama API with the prompt to generate a code solution.
5.  **Code Extraction:** The Python code is parsed from the model's response.
6.  **Execution and Validation:** The extracted code is executed against a series of test cases.
7.  **Metric Collection:** Performance data from both generation and execution are logged.
8.  **Reporting:** Results are displayed in a summary table and saved to detailed log files.

## Getting Started

Follow these instructions to set up and run the evaluator on your local machine.

### Prerequisites

*   Python 3.9 or higher
*   [Ollama](https://ollama.ai/) installed and running
*   At least one model installed via Ollama (e.g., `ollama run llama3`)

### Installation

1.  **Clone the repository:**
    ```sh
    git clone https://github.com/your-username/llm-code-evaluator.git
    cd llm-code-evaluator
    ```
2.  **Install the required Python packages:**
    ```sh
    pip install -r requirements.txt
    ```
    *(Note: You will need to create a `requirements.txt` file containing `ollama`, `questionary`, and `rich`)*

## Usage

1.  **Ensure Ollama is running:**
    Open a new terminal and start the Ollama service.
    ```sh
    ollama serve
    ```

2.  **Run the evaluation script:**
    ```sh
    python dual_method_eval.py
    ```

3.  **Follow the interactive prompts:**
    *   Select the model you wish to evaluate.
    *   Choose an output style for the model's responses.
    *   Select an action, such as running all problems, a single problem, or viewing the report.

## File Descriptions

*   **`dual_method_eval.py`**: The main script that orchestrates the evaluation process.
*   **`helpers.py`**: Contains utility functions for handling complex data structures like binary trees.
*   **`problems.json`**: A JSON file containing the coding problems, their prompts, and test cases.
*   **`logs/`**: The directory where all session logs and reports are saved.

## Output

The tool generates two primary forms of output:

1.  **Console Report:** A summary table is printed to the console at the end of the session, showing key performance indicators for each test run.
2.  **Log Files:** For each session, a detailed `.txt` log and a summary `.csv` report are saved in the `logs/` directory, named with the session's timestamp.

## Contributing

Contributions are welcome! Please read the [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct and the process for submitting pull requests.

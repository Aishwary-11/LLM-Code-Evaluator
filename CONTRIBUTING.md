# Contributing to the LLM Code Evaluator

First off, thank you for considering contributing! Your help is invaluable in making this tool better for everyone. Every contribution, from a small typo fix to a new feature, is welcome.

This document provides guidelines for contributing to this project. Following them helps to ensure that the contribution process is smooth and that the project remains consistent and easy to maintain.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [How Can I Contribute?](#how-can-i-contribute)
  - [Reporting Bugs](#reporting-bugs)
  - [Suggesting Enhancements](#suggesting-enhancements)
  - [Adding New Problems](#adding-new-problems)
  - [Submitting a Pull Request](#submitting-a-pull-request)
- [Development Setup](#development-setup)
- [Pull Request Guidelines](#pull-request-guidelines)
- [Styleguides](#styleguides)

## Code of Conduct

This project and everyone participating in it is governed by the [Code of Conduct](CODE_OF_CONDUCT.md). By participating, you are expected to uphold this code. Please report unacceptable behavior to the project maintainers.



## How Can I Contribute?

### Reporting Bugs

If you find a bug, please ensure it hasn't already been reported by searching the [Issues](https://github.com/your-username/llm-code-evaluator/issues) on GitHub.

If you're unable to find an open issue addressing the problem, open a [new one](https://github.com/your-username/llm-code-evaluator/issues/new). Be sure to include:

- A **clear and descriptive title**.
- A detailed description of the bug, including the **steps to reproduce it**.
- The **expected behavior** and what happened instead.
- Your **operating system, Python version, and Docker version** (if applicable).
- Any relevant **log output or screenshots**.

### Suggesting Enhancements

If you have an idea for a new feature or an improvement to an existing one:

1.  Check the [Issues](https://github.com/your-username/llm-code-evaluator/issues) to see if the enhancement has already been suggested.
2.  If not, open a new issue with a clear title and a detailed description of the proposed enhancement and why it would be beneficial.

### Adding New Problems

This is one of the easiest and most impactful ways to contribute! To add a new coding problem:

1.  Open the `problems.json` file.
2.  Copy an existing problem object to use as a template.
3.  Add a new JSON object to the main array with the following fields:
    - `title`: (String) The name of the problem (e.g., "Two Sum").
    - `prompt`: (String) The full prompt to be sent to the LLM. This should clearly state the problem and constraints.
    - `method_name`: (String) The exact name of the method the LLM should create within the `Solution` class (e.g., `twoSum`).
    - `test_cases`: (Array) A list of test case objects.
        - Each test case is an object with an `input` object and an `output` value.
        - The keys in the `input` object must match the parameter names of the method.
    - `inplace_modification`: (Boolean, optional) Set to `true` if the method modifies an input list/array in place instead of returning a new value.
    - `output_is_tree`: (Boolean, optional) Set to `true` if the method's return value is a binary tree that needs to be converted to a list for comparison.

**Example Problem Structure:**
```json
{
    "title": "Your Problem Title",
    "prompt": "Provide a Python solution...",
    "method_name": "yourMethodName",
    "inplace_modification": false,
    "output_is_tree": false,
    "test_cases": [
        {"input": {"nums":, "target": 3}, "output":},
        {"input": {"nums":, "target": 10}, "output":}
    ]
}

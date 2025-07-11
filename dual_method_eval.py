import ollama
import sys
import time
import json
import re
import os
import csv
from datetime import datetime
from rich.console import Console
from rich.table import Table
from rich.progress import track
import questionary

# Import helpers for tree problems
from helpers import TreeNode, build_tree, tree_to_list

# --- Configuration and Setup ---
OLLAMA_HOST = "http://127.0.0.1:11434"
LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)
SESSION_TIMESTAMP = datetime.now().strftime("%Y%m%d_%H%M%S")
LOG_FILENAME = os.path.join(LOG_DIR, f"sdk_session_log_{SESSION_TIMESTAMP}.txt")
REPORT_FILENAME = os.path.join(LOG_DIR, f"session_report_{SESSION_TIMESTAMP}.csv")


console = Console()

OUTPUT_STYLES = [
    {
        "name": "Default (Unstructured)",
        "template": ""
    },
    {
        "name": "Code Only",
        "template": "Provide only the complete Python code block inside a class `Solution`. Do not include any explanations, introductory text, or concluding remarks."
    },
    {
        "name": "Code with Brief Explanation",
        "template": "Provide the complete Python code block first. Afterwards, provide a brief explanation of the overall approach."
    },
    {
        "name": "Code with Detailed Explanation",
        "template": "Provide the complete Python code block first. Then, provide a detailed, step-by-step explanation of the algorithm, including its time and space complexity."
    }
]


def load_problems_from_json(filename="problems.json"):
    """Loads problems and test cases from a JSON file."""
    try:
        with open(filename, "r", encoding="utf-8") as f:
            problems = json.load(f)
        console.print(f"[green]Successfully loaded {len(problems)} problems from '{filename}'[/green]")
        return problems
    except FileNotFoundError:
        console.print(f"[bold red]ERROR: The file '{filename}' was not found.[/bold red]")
        sys.exit(1)
    except json.JSONDecodeError:
        console.print(f"[bold red]ERROR: The file '{filename}' contains invalid JSON.[/bold red]")
        sys.exit(1)


def parse_code_from_response(response: str) -> str | None:
    """Extracts Python code from a markdown code block."""
    match = re.search(r"```python\n(.*?)```", response, re.DOTALL)
    if match:
        return match.group(1).strip()
    if "class Solution:" in response:
        
        return response.strip()
    return None

def run_tests_for_solution(code_string: str, problem: dict) -> dict:
    """
    Executes code against test cases and returns a dictionary of evaluation metrics.
    CAUTION: This function uses exec() and should only be used with trusted LLM outputs.
    """
    
    default_metrics = {
        "passed_count": 0, "total_tests": len(problem.get("test_cases", [])),
        "execution_time_ms": -1, "code_lines": 0,
        "status_message": "[bold red]Code Parsing Failed[/bold red]"
    }

    if not code_string:
        return default_metrics
    
    
    default_metrics["code_lines"] = len(code_string.splitlines())

    test_cases = problem.get("test_cases", [])
    if not test_cases:
        default_metrics["status_message"] = "[yellow]No Test Cases[/yellow]"
        return default_metrics

    passed_count = 0
    execution_globals = {"TreeNode": TreeNode, "build_tree": build_tree}
    
    try:
        exec(code_string, execution_globals)
        SolutionClass = execution_globals.get('Solution')
        if not SolutionClass:
            default_metrics["status_message"] = "[bold red]Execution Error: 'Solution' class not found[/bold red]"
            return default_metrics

       
        start_time = time.perf_counter()

        for test in test_cases:
            solver = SolutionClass()
            method_to_test = getattr(solver, problem["method_name"])
            
            raw_input = test["input"].copy()
            processed_input = {k: build_tree(v) if isinstance(v, list) and ("tree" in k or k in ["p", "q", "root"]) else v for k, v in raw_input.items()}

            if problem.get("inplace_modification"):
                method_to_test(**processed_input)
                actual_output = raw_input['nums']
            else:
                actual_output = method_to_test(**processed_input)
            
            if problem.get("output_is_tree"):
                actual_output = tree_to_list(actual_output)

            if actual_output == test["output"]:
                passed_count += 1
        
        end_time = time.perf_counter()
        execution_time_ms = (end_time - start_time) * 1000

       
        status_message = f"[bold green]Passed[/]" if passed_count == len(test_cases) else f"[bold yellow]Failed[/]"
        
        return {
            "passed_count": passed_count,
            "total_tests": len(test_cases),
            "execution_time_ms": execution_time_ms,
            "code_lines": default_metrics["code_lines"],
            "status_message": f"{status_message} {passed_count}/{len(test_cases)}"
        }

    except Exception as e:
        default_metrics["status_message"] = f"[bold red]Execution Error: {type(e).__name__}[/bold red]"
        return default_metrics




def get_available_models(host: str) -> list:
    """Fetches the list of all available models using the SDK."""
    try:
        console.print("Fetching available models from Ollama...")
        client = ollama.Client(host=host)
        models_list = [model.get("model") for model in client.list().get("models", [])]
        if not models_list:
            console.print("  [yellow]No models found on the Ollama server.[/yellow]")
            return []
        return models_list
    except Exception as e:
        console.print(f"  [bold red]ERROR fetching models: {e}[/bold red]")
        return []

def select_from_list(name: str, choices: list, current_value: str = None) -> str:
    """Generic function to display an interactive list and get a selection."""
    if not choices: return None
    message = f"Select a {name}"
    if current_value: message = f"Current {name} is '{current_value}'. Change it?"
    return questionary.select(message, choices=choices, use_indicator=True).ask()

def call_sdk(prompt: str, model_name: str) -> tuple:
    """Gets a response and stats using the Python SDK."""
    start_time = time.time()
    try:
        client = ollama.Client(host=OLLAMA_HOST, timeout=300)
        response = client.generate(model=model_name, prompt=prompt, stream=False)
        end_time = time.time()
        text = response.get("response", "Error: No response text found.").strip()
        stats = {
            "time_taken": f"{(end_time - start_time):.2f}",
            "prompt_tokens": response.get("prompt_eval_count", 0),
            "completion_tokens": response.get("eval_count", 0),
        }
        return text, stats
    except Exception as e:
        return f"An error occurred: {e}", {}

def run_problem(problem: dict, model_name: str, style: dict, session_log: list):
    """Runs a single problem, tests the code, and updates the session log."""
    console.print(f"--- Running Problem: [bold cyan]{problem['title']}[/bold cyan] ---")
    
    final_prompt = f"{problem['prompt']}\n\n{style['template']}".strip()
    response, gen_stats = call_sdk(final_prompt, model_name)
    
    code = parse_code_from_response(response)
    eval_metrics = run_tests_for_solution(code, problem)

    
    console.print(f"  - Generation Time: {gen_stats.get('time_taken', 'N/A')}s, Tokens (P/C): {gen_stats.get('prompt_tokens', 0)}/{gen_stats.get('completion_tokens', 0)}")
    console.print(f"  - Validation: {eval_metrics['status_message']}")
    if eval_metrics['execution_time_ms'] >= 0:
        console.print(f"  - Performance: {eval_metrics['execution_time_ms']:.4f} ms, Code Length: {eval_metrics['code_lines']} LoC")

    
    session_log.append({
        "problem": problem['title'],
        "model": model_name,
        "style": style['name'],
        "test_result": re.sub(r'\[.*?\]', '', eval_metrics['status_message']), # Strip rich tags
        "passed_count": eval_metrics['passed_count'],
        "total_tests": eval_metrics['total_tests'],
        "exec_time_ms": f"{eval_metrics['execution_time_ms']:.4f}" if eval_metrics['execution_time_ms'] >= 0 else "N/A",
        "code_lines": eval_metrics['code_lines'] if eval_metrics['code_lines'] > 0 else "N/A",
        "gen_time_s": gen_stats.get('time_taken', 'N/A'),
        "prompt_tokens": gen_stats.get('prompt_tokens', 'N/A'),
        "completion_tokens": gen_stats.get('completion_tokens', 'N/A'),
        "full_prompt": final_prompt,
        "full_response": response,
    })


def save_session_log(session_log: list):
    """Saves the detailed session results to a text file."""
    if not session_log: return
    with open(LOG_FILENAME, "w", encoding="utf-8") as f:
        f.write(f"Python SDK Evaluation Session Log - {SESSION_TIMESTAMP}\n\n")
        
    console.print(f"\n[green]Detailed session log saved to:[/] [bold]{LOG_FILENAME}[/bold]")

def display_session_report(session_log: list):
    """Displays a summary report table with the new evaluation criteria."""
    if not session_log:
        console.print("[yellow]No results to display in the report.[/yellow]")
        return

    table = Table(title="Session Summary Report")
    table.add_column("Problem", style="cyan")
    table.add_column("Model", style="magenta")
    table.add_column("Result", justify="center")
    
    table.add_column("Exec Time (ms)", justify="right", style="blue")
    table.add_column("LoC", justify="right", style="blue")
    
    table.add_column("Gen Time (s)", justify="right", style="green")
    table.add_column("Tokens (C)", justify="right", style="green")

    for entry in session_log:
        result_str = re.sub(r'\[.*?\]', '', entry['test_result']) 
        if "Passed" in result_str: color_result = f"[bold green]{result_str}[/]"
        elif "Failed" in result_str: color_result = f"[bold yellow]{result_str}[/]"
        else: color_result = f"[bold red]{result_str}[/]"

        table.add_row(
            entry['problem'],
            entry['model'],
            color_result,
            str(entry['exec_time_ms']),
            str(entry['code_lines']),
            str(entry['gen_time_s']),
            str(entry['completion_tokens']),
        )
    console.print(table)

def save_report_as_csv(session_log: list):
    """Saves the summary report to a CSV file."""
    if not session_log: return
    
    
    report_data = []
    for entry in session_log:
        clean_entry = {k: v for k, v in entry.items() if k not in ["full_prompt", "full_response"]}
        report_data.append(clean_entry)

    with open(REPORT_FILENAME, 'w', newline='', encoding='utf-8') as f:
        if report_data:
            writer = csv.DictWriter(f, fieldnames=report_data[0].keys())
            writer.writeheader()
            writer.writerows(report_data)
    console.print(f"[green]Summary report saved as CSV to:[/] [bold]{REPORT_FILENAME}[/bold]")


if __name__ == "__main__":
    console.print("[bold purple]--- Ollama SDK Advanced Problem Evaluator ---[/bold purple]")
    
    ALL_PROBLEMS = load_problems_from_json()
    available_models = get_available_models(OLLAMA_HOST)
    if not available_models: sys.exit(1)

    current_model = select_from_list("model", available_models)
    if not current_model: sys.exit(1)

    current_style = select_from_list("style", [s['name'] for s in OUTPUT_STYLES])
    if not current_style: sys.exit(1)
    
    session_log = []

    while True:
        console.print("\n" + "="*50)
        console.print(f"Active Model: [bold magenta]{current_model}[/bold magenta]")
        console.print(f"Active Style: [bold blue]{current_style}[/bold blue]")

        choice = questionary.select(
            "Choose an action:",
            choices=["Run All Problems", "Pick a Problem to Run", "Change Model", "Set Style", "View Session Report", "Quit and Save"],
            use_indicator=True
        ).ask()

        if choice is None or choice == "Quit and Save":
            break
        
        elif choice == "Change Model":
            current_model = select_from_list("model", available_models, current_model) or current_model

        elif choice == "Set Style":
            current_style = select_from_list("style", [s['name'] for s in OUTPUT_STYLES], current_style) or current_style

        elif choice == "Run All Problems" or choice == "Pick a Problem to Run":
            problems_to_run = []
            if choice == "Run All Problems":
                problems_to_run = ALL_PROBLEMS
                console.print(f"\n[bold]Starting bulk run for model: '{current_model}' with style: '{current_style}'[/bold]")
            else:
                problem_title = select_from_list("problem", [p['title'] for p in ALL_PROBLEMS])
                if problem_title:
                    problems_to_run.append(next(p for p in ALL_PROBLEMS if p['title'] == problem_title))
            
            if problems_to_run:
                style_obj = next(s for s in OUTPUT_STYLES if s['name'] == current_style)
                for problem in track(problems_to_run, description="Processing problems..."):
                    run_problem(problem, current_model, style_obj, session_log)
                    time.sleep(1)
                console.print("\n[bold green]Run completed![/bold green]")
        
        elif choice == "View Session Report":
            display_session_report(session_log)

    
    console.print("\n[bold purple]--- Session Finished ---[/bold purple]")
    if session_log:
        display_session_report(session_log)
        save_session_log(session_log)
        if questionary.confirm("Save summary report as CSV?").ask():
            save_report_as_csv(session_log)
    else:
        console.print("[yellow]No actions were run, so no logs were created.[/yellow]")

    console.print("Goodbye!")

import typer
import json
from rich import print
from tests.run_all import main as run_tests

app = typer.Typer()

FILE_PATH = "tests/sample_tests.json"


@app.command()
def run():
    """
    Run all LLM tests
    """
    run_tests()


@app.command()
def list():
    """
    List all test cases
    """
    try:
        with open(FILE_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)

        print("\n[bold cyan]📋 Available Tests:[/bold cyan]\n")

        if not data:
            print("[yellow]No tests found[/yellow]\n")
            return

        for i, test in enumerate(data, start=1):
            rules = [r["type"] for r in test.get("rules", [])]
            print(f"[yellow]{i}.[/yellow] {test['name']} [dim](rules: {rules})[/dim]")

        print("")

    except FileNotFoundError:
        print("[red]❌ sample_tests.json not found[/red]")


@app.command()
def add(name: str, prompt: str):
    """
    Add a new test case
    """
    try:
        with open(FILE_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)

    except FileNotFoundError:
        data = []

    # 🔥 Default rule (can extend later)
    new_test = {
        "name": name,
        "prompt": prompt,
        "rules": [
            {
                "type": "json_valid",
                "params": {}
            }
        ]
    }

    data.append(new_test)

    with open(FILE_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

    print(f"[green]✅ Added test:[/green] {name}")


if __name__ == "__main__":
    app()
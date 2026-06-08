import json
from rich import print
from core.models import TestCase
from core.executor import run_test_case


def main():
    with open("tests/sample_tests.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    tests = [TestCase(**t) for t in data]

    print(f"\n🚀 [bold]Running {len(tests)} tests...[/bold]\n")

    passed_count = 0
    failed_count = 0

    for i, test in enumerate(tests, start=1):
        print(f"\n➡️ [cyan]Test {i}/{len(tests)}:[/cyan] {test.name}")

        result = run_test_case(test)

        if result["passed"]:
            passed_count += 1
        else:
            failed_count += 1

    # 🔥 FINAL SUMMARY
    print("\n===================================")
    print("[bold]📊 TEST SUMMARY[/bold]")
    print("===================================")

    print(f"[green]✅ Passed:[/green] {passed_count}")
    print(f"[red]❌ Failed:[/red] {failed_count}")
    print(f"📦 Total:  {len(tests)}")

    # 🎯 Success rate
    success_rate = round((passed_count / len(tests)) * 100, 2)
    print(f"\n🎯 Success Rate: {success_rate}%")

    # 🚨 Final system status
    if failed_count > 0:
        print("[bold red]⚠ Some tests failed — investigate issues[/bold red]")
    else:
        print("[bold green]🚀 All tests passed — system stable[/bold green]")

    print("===================================\n")


if __name__ == "__main__":
    main()
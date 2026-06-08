# ===============================
# 🔹 IMPORTS
# ===============================
from core.runner import run_prompt
from core.rules import evaluate_rules, final_decision
from core.database import SessionLocal, Result
from core.diff_engine import (
    compute_similarity,
    json_diff,
    detect_regression,
    cosine_similarity,
)
from core.embedding import get_embedding
from rich import print


# ===============================
# 🔹 MAIN EXECUTION FUNCTION
# ===============================
def run_test_case(test):
    """Execute a single regression test."""

    result = run_prompt(test.prompt)

    output = result.get("output", "").strip()
    latency = result.get("latency")
    error = result.get("error")

    # ===============================
    # 🔹 ERROR HANDLING
    # ===============================
    if error or not output:
        print(f"\n[bold red]Test:[/bold red] {test.name}")
        print(f"[red]Error:[/red] {error or 'Empty output'}")

        return {
            "passed": False,
            "latency": latency,
            "similarity": None,
            "regression": False,
            "expected_similarity": None,
        }

    # ===============================
    # 🔹 RULE VALIDATION
    # ===============================
    rule_results = evaluate_rules(output, test.rules)
    rules_passed = final_decision(rule_results)

    db = SessionLocal()

    try:
        # ===============================
        # 🔹 LOAD PREVIOUS OUTPUT
        # ===============================
        prev = (
            db.query(Result)
            .filter_by(test_name=test.name)
            .order_by(Result.id.desc())
            .first()
        )

        previous_output = prev.output if prev else None

        # ===============================
        # 🔹 REGRESSION CHECK
        # ===============================
        similarity = None
        embedding_similarity = None
        diff_result = None
        regression = False

        if previous_output:
            vec1 = get_embedding(previous_output)
            vec2 = get_embedding(output)

            if vec1 and vec2:
                embedding_similarity = cosine_similarity(vec1, vec2)

            similarity = compute_similarity(
                previous_output,
                output,
                embedding_similarity,
            )

            diff_result = json_diff(previous_output, output)

            if similarity is not None:
                regression = detect_regression(similarity)

        # ===============================
        # 🔹 EXPECTED OUTPUT CHECK (ONLY FOR DISPLAY)
        # ===============================
        expected_similarity = None
        expected_fail = False
        threshold = getattr(test, "expected_similarity_threshold", 0.8)

        if test.expected_output:
            expected_similarity = compute_similarity(
                test.expected_output,
                output
            )

            if expected_similarity < threshold:
                expected_fail = True

        # ===============================
        # 🔥 FINAL PASS DECISION (CORRECT)
        # ===============================
        if test.rules:
            # ✅ RULES ALWAYS WIN
            passed = rules_passed

        elif test.expected_output:
            # Only when NO rules
            passed = not expected_fail

        else:
            passed = True

        # ===============================
        # 🔹 PRINT OUTPUT
        # ===============================
        print(f"\n[bold cyan]Test:[/bold cyan] {test.name}")
        print("[green]PASS[/green]" if passed else "[red]FAIL[/red]")

        for rule in rule_results:
            icon = "[green]✔[/green]" if rule["passed"] else "[red]✖[/red]"
            print(f"{icon} {rule['rule']}")

        print(f"[blue]Latency:[/blue] {latency}s")

        # Regression info
        if similarity is not None:
            print(f"[magenta]Similarity:[/magenta] {round(similarity, 3)}")

            if regression:
                print("[bold red]🚨 Regression Detected[/bold red]")
            elif similarity < 0.95:
                print("[yellow]⚠ Minor Change[/yellow]")

        if embedding_similarity is not None:
            print(f"[cyan]Semantic Similarity:[/cyan] {round(embedding_similarity, 3)}")

        # Expected (only display)
        if test.expected_output:
            print(f"[blue]Expected Similarity:[/blue] {round(expected_similarity, 3)}")

            if expected_fail:
                print("[bold red]🚨 Output Deviates from Expected[/bold red]")

        # JSON diff
        if diff_result:
            if diff_result.get("missing_keys"):
                print(f"[red]Missing Keys:[/red] {diff_result['missing_keys']}")

            if diff_result.get("changed_keys"):
                print(f"[yellow]Changed Keys:[/yellow] {diff_result['changed_keys']}")

            if diff_result.get("added_keys"):
                print(f"[cyan]Added Keys:[/cyan] {diff_result['added_keys']}")

        print(f"\n[yellow]Output:[/yellow]\n{output}")

        # ===============================
        # 🔹 SAVE RESULT
        # ===============================
        db.add(
            Result(
                test_name=test.name,
                prompt=test.prompt,
                output=output,
                previous_output=previous_output,
                latency=latency,
            )
        )

        db.commit()

    finally:
        db.close()

    return {
        "passed": passed,
        "latency": latency,
        "similarity": similarity,
        "regression": regression,
        "expected_similarity": expected_similarity,
    }
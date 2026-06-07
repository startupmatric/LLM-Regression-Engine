from core.runner import run_prompt
from core.rules import evaluate_rules, final_decision
from core.database import SessionLocal, Result


def run_test_case(test):
    output = run_prompt(test.prompt)

    rule_results = evaluate_rules(output, test.rules)
    passed = final_decision(rule_results)

    print(f"\n🧪 Test: {test.name}")
    print("✅ PASS" if passed else "❌ FAIL")

    for r in rule_results:
        status = "✔️" if r["passed"] else "❌"
        print(f" - {r['rule']}: {status}")

    print(f"\n📤 Output:\n{output}")
    print("-" * 50)

    # Save to DB
    db = SessionLocal()
    db.add(Result(
        test_name=test.name,
        prompt=test.prompt,
        output=output
    ))
    db.commit()
    db.close()

    # 🔥 CRITICAL FIX: return result
    return {
        "passed": passed
    }
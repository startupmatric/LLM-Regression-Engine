import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import json
from core.models import TestCase
from core.executor import run_test_case


def main():
    with open("tests/sample_tests.json") as f:
        data = json.load(f)

    tests = [TestCase(**t) for t in data]

    print(f"\n🚀 Running {len(tests)} tests...\n")

    passed_count = 0
    failed_count = 0

    for i, test in enumerate(tests, start=1):
        print(f"\n➡️ Test {i}/{len(tests)}: {test.name}")

        result = run_test_case(test)

        if result["passed"]:
            passed_count += 1
        else:
            failed_count += 1

    # 🔥 FINAL SUMMARY (CORRECT)
    print("\n===================================")
    print("📊 TEST SUMMARY")
    print("===================================")
    print(f"✅ Passed: {passed_count}")
    print(f"❌ Failed: {failed_count}")
    print(f"📦 Total:  {len(tests)}")
    print("===================================")


if __name__ == "__main__":
    main()
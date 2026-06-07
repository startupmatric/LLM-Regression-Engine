import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import json
from core.models import TestCase

with open("tests/sample_tests.json", "r", encoding="utf-8") as f:
    data = json.load(f)

tests = [TestCase(**item) for item in data]

print(f"\nLoaded {len(tests)} tests\n")

for test in tests:
    print(f"Test: {test.name}")

    for rule in test.rules:
        print(f"  - Rule: {rule.type} | Params: {rule.params}")

print("\n✅ All tests validated successfully")
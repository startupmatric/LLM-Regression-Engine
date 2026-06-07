import json

def check_json_valid(output: str) -> bool:
    output = output.strip()

    if "```" in output:
        return False

    if not (output.startswith("{") or output.startswith("[")):
        return False

    if not (output.endswith("}") or output.endswith("]")):
        return False

    try:
        parsed = json.loads(output)
        return isinstance(parsed, (dict, list))
    except:
        return False


def check_contains_keyword(output: str, word: str) -> bool:
    return word.lower() in output.lower()


def check_max_length(output: str, limit: int) -> bool:
    return len(output.split()) <= limit


def evaluate_rules(output: str, rules: list):
    results = []

    for rule in rules:
        if rule.type == "json_valid":
            passed = check_json_valid(output)

        elif rule.type == "contains_keyword":
            passed = check_contains_keyword(output, rule.params.get("word", ""))

        elif rule.type == "max_length":
            passed = check_max_length(output, rule.params.get("limit", 100))

        else:
            passed = True

        results.append({
            "rule": rule.type,
            "passed": passed
        })

    return results


def final_decision(rule_results):
    return all(r["passed"] for r in rule_results)
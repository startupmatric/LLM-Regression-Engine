import json
import re


# -------------------------------
# 🔥 JSON VALIDATION
# -------------------------------
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
    except json.JSONDecodeError:
        return False


# -------------------------------
# 🔥 KEYWORD CHECK
# -------------------------------
def check_contains_keyword(output: str, word: str) -> bool:
    return word.lower() in output.lower() if word else True


# -------------------------------
# 🔥 LENGTH CHECK
# -------------------------------
def check_max_length(output: str, limit: int) -> bool:
    words = re.findall(r"\b\w+\b", output)
    return len(words) <= limit


def check_min_length(output: str, limit: int) -> bool:
    words = re.findall(r"\b\w+\b", output)
    return len(words) >= limit


# -------------------------------
# 🔥 NOT CONTAINS
# -------------------------------
def check_not_contains(output: str, word: str) -> bool:
    return word.lower() not in output.lower() if word else True


# -------------------------------
# 🔥 FORMAT CHECK
# -------------------------------
def check_format(output: str, format_type: str) -> bool:
    lines = output.strip().splitlines()

    if format_type == "bullet_points":
        return any(line.strip().startswith(("-", "*", "•")) for line in lines)

    if format_type == "numbered_list":
        return any(re.match(r"\d+\.", line.strip()) for line in lines)

    if format_type == "paragraph":
        return len(lines) <= 2

    if format_type == "sections":
        return any(line.strip().startswith(("##", "###")) or line.strip().isupper() for line in lines)

    return True


# -------------------------------
# 🔥 RULE ENGINE
# -------------------------------
def evaluate_rules(output: str, rules: list):
    if not output.strip():
        return [{"rule": "empty_output", "passed": False}]

    results = []

    for rule in rules:
        rule_type = getattr(rule, "type", None)
        params = getattr(rule, "params", {}) or {}

        try:
            if rule_type == "json_valid":
                passed = check_json_valid(output)

            elif rule_type == "contains_keyword":
                passed = check_contains_keyword(output, params.get("word", ""))

            elif rule_type == "max_length":
                passed = check_max_length(output, params.get("limit", 100))

            elif rule_type == "min_length":
                passed = check_min_length(output, params.get("limit", 1))

            elif rule_type == "not_contains":
                passed = check_not_contains(output, params.get("word", ""))

            elif rule_type == "format":
                passed = check_format(output, params.get("type", ""))

            else:
                passed = True

        except Exception:
            passed = False

        results.append({
            "rule": rule_type,
            "passed": passed
        })

    return results


# -------------------------------
# 🔥 FINAL DECISION (ONLY RULES)
# -------------------------------
def final_decision(rule_results):
    return all(r["passed"] for r in rule_results)
import json
import re
import math
from difflib import SequenceMatcher


# -------------------------------
# 🔥 NORMALIZE TEXT
# -------------------------------
def normalize_text(text: str) -> str:
    text = text.lower()
    text = re.sub(r"\s+", " ", text)
    return text.strip()


# -------------------------------
# 🔥 STRING SIMILARITY
# -------------------------------
def string_similarity(a: str, b: str) -> float:
    a = normalize_text(a)
    b = normalize_text(b)
    return SequenceMatcher(None, a, b).ratio()


# -------------------------------
# 🔥 JSON STRUCTURE SIMILARITY
# -------------------------------
def json_similarity(old: str, new: str):
    try:
        old_json = json.loads(old)
        new_json = json.loads(new)

        old_keys = set(old_json.keys())
        new_keys = set(new_json.keys())

        intersection = len(old_keys & new_keys)
        union = len(old_keys | new_keys)

        return intersection / union if union > 0 else 0

    except:
        return None


# -------------------------------
# 🔥 COSINE SIMILARITY (EMBEDDINGS)
# -------------------------------
def cosine_similarity(vec1, vec2):
    dot = sum(a * b for a, b in zip(vec1, vec2))
    mag1 = math.sqrt(sum(a * a for a in vec1))
    mag2 = math.sqrt(sum(b * b for b in vec2))

    if mag1 == 0 or mag2 == 0:
        return 0

    return dot / (mag1 * mag2)


# -------------------------------
# 🔥 FINAL HYBRID SIMILARITY
# -------------------------------
def compute_similarity(old: str, new: str, embedding_score: float = None) -> float:
    str_sim = string_similarity(old, new)
    json_sim = json_similarity(old, new)

    # Base score
    if json_sim is not None:
        base_score = (0.6 * str_sim) + (0.4 * json_sim)
    else:
        base_score = str_sim

    # If embedding available → include it
    if embedding_score is not None:
        final_score = (0.5 * base_score) + (0.5 * embedding_score)
    else:
        final_score = base_score

    return round(final_score, 3)


# -------------------------------
# 🔥 JSON DIFF (STRUCTURE)
# -------------------------------
def json_diff(old: str, new: str):
    try:
        old_json = json.loads(old)
        new_json = json.loads(new)

        missing_keys = []
        changed_keys = []
        added_keys = []

        for key in old_json:
            if key not in new_json:
                missing_keys.append(key)
            elif old_json[key] != new_json[key]:
                changed_keys.append(key)

        for key in new_json:
            if key not in old_json:
                added_keys.append(key)

        return {
            "missing_keys": missing_keys,
            "changed_keys": changed_keys,
            "added_keys": added_keys
        }

    except:
        return None


# -------------------------------
# 🔥 REGRESSION CHECK
# -------------------------------
def detect_regression(similarity: float, threshold: float = 0.85):
    if similarity is None:
        return False
    return similarity < threshold
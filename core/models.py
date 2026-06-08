from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


# -------------------------------
# 🔥 PRIORITY ENUM
# -------------------------------
class Priority(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"


# -------------------------------
# 🔥 RULE MODEL
# -------------------------------
class Rule(BaseModel):
    type: str
    params: Dict[str, Any] = Field(default_factory=dict)


# -------------------------------
# 🔥 TEST CASE MODEL
# -------------------------------
class TestCase(BaseModel):
    name: str
    description: Optional[str] = None

    prompt: str

    # 🔥 Expected output (for similarity comparison)
    expected_output: Optional[str] = None

    # 🔥 Optional threshold for similarity
    expected_similarity_threshold: Optional[float] = 0.8

    rules: List[Rule] = Field(default_factory=list)

    tags: List[str] = Field(default_factory=list)

    priority: Priority = Priority.medium

    version: int = 1

    # -------------------------------
    # 🔥 GET RULE HELPER
    # -------------------------------
    def get_rule(self, rule_type: str):
        for rule in self.rules:
            if rule.type == rule_type:
                return rule
        return None
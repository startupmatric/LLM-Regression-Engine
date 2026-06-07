from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class Priority(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"


class Rule(BaseModel):
    type: str
    params: Dict[str, Any] = Field(default_factory=dict)


class TestCase(BaseModel):
    name: str
    description: Optional[str] = None

    prompt: str

    expected_output: Optional[str] = None

    rules: List[Rule] = Field(default_factory=list)

    tags: List[str] = Field(default_factory=list)

    priority: Priority = Priority.medium

    version: int = 1

    def get_rule(self, rule_type: str):
        for rule in self.rules:
            if rule.type == rule_type:
                return rule
        return None
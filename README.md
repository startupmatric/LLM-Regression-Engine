# 🧠 LLM Regression Engine

> CI/CD guardrails for LLM applications.

Detect silent failures, behavioral drift, and broken outputs in AI systems before they reach production.

## 🚨 Problem

LLM applications break silently:

* JSON outputs fail
* hallucinations increase
* tone changes
* logic becomes inconsistent

## 💡 Solution

A regression testing system for LLMs:

* Store baseline outputs
* Re-run prompts on new models
* Detect drift using similarity + rules
* Fail builds if behavior changes

## ⚙️ Features (MVP)

* Prompt test registry
* LLM runner
* Diff engine (semantic + structural)
* Rule-based validation
* CLI for test execution

## 🎯 Vision

“PyTest for LLM applications.”

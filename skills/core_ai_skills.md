# Core AI Developer Skills & Architecture Guide

This document outlines the core AI skills, agentic workflows, parsing paradigms, and self-healing techniques employed in the **SQL Insights** application.

---

## 🤖 LLM Client Integration & Prompt Architecture

### Local Model Orchestration (Ollama Client)
- **Model Target:** Uses local LLM orchestrations (configured via `OLLAMA_URL` and `OLLAMA_MODEL` defaults, e.g., `phi:latest`).
- **Prompt Isolation:** Design prompt formats specifically structured to elicit structured outputs, using rules to suppress markdown code fences and explanations.

### Agent Prompts & Context Windows
- **System Instructions:** Directives that force output types (e.g., `"Return ONLY raw SQL. NO explanations, comments, or extra text"`).
- **Context Injection:** Injecting dynamic table schema definitions into the context window for high-precision query generation.

---

## 🛠️ Key Agent Design & Logic

### 1. SQL Generation Agent (`sql_agent.py`)
- **Natural Language Parsing:** Maps general intent to valid database commands (PostgreSQL syntax is standard).
- **Post-Processing & Sanitization:** Regex-based parsers extract query text, drop markdown wrappers (like ` ```sql ` blocks), and sanitize SQL syntax.
- **Safety Validators:** Verifies that queries only reference known columns within the schema catalog to prevent database model hallucinations.

### 2. SQL Self-Healing (`self_heal_sql`)
- **Execution Loop Feedback:** When database execution fails, the faulty SQL query and database engine error trace are packaged back to the agent in a self-healing loop.
- **Auto-Correction Prompt:** Instructs the LLM to analyze the schema constraints, inspect the failure reason, and produce a corrected, runnable SQL query.

### 3. Intent, Schema & Visualization Agents
- **Intent Classifier:** Classifies if query needs visual charts, PDF reporting, or simple text analytics.
- **Visualization Agent:** Determines the optimal visual structure (chart types, aggregations) and structures JSON schema data for the frontend.
- **Analysis Agent:** Converts tabular dataset findings into human-readable insights, trends, and business conclusions.

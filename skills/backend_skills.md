# Backend Developer Skills & Architecture Guide

This document outlines the core skills, technologies, and patterns required to build and maintain the backend of the **SQL Insights** application.

---

## ⚙️ Core Technology Stack

### 1. Python & FastAPI
- **Web Framework:** High-performance async APIs built with FastAPI.
- **Data Validation:** Pydantic models for request/response serialization and configuration settings (`pydantic-settings`).
- **Dependency Injection:** Modular service injection for settings, database engines, and client connections.

### 2. Large Language Models (LLM) Integration
- **Ollama:** Interfacing with local LLMs (e.g., `phi:latest`) for private and secure natural language processing.
- **Prompt Engineering:** Structuring zero-shot and few-shot prompts to enforce precise output formats like structured JSON or raw SQL query blocks.

### 3. Database Management & Safety
- **SQLAlchemy & Databases:** DB connection abstraction for PostgreSQL (`psycopg2-binary`) and MySQL (`pymysql`).
- **Read-Only Enforcement:** Strict safety validation of dynamically generated SQL queries to prevent write/delete operations (e.g. denying statements containing `DROP`, `DELETE`, `INSERT`, `UPDATE`, `ALTER`).

### 4. Data Processing & Visualization
- **Pandas:** Tabulating, cleaning, and transforming SQL result sets.
- **Plotly & Visualization Agent:** Converting pandas DataFrames into visualization schemas for rendering on the frontend.
- **ReportLab PDF Generation:** Generating pixel-perfect PDF reports containing data tables, text insights, and visualizations for export.

---

## 🤖 Multi-Agent Architecture

The backend implements a modular Multi-Agent workflow:

1. **Intent Agent:** Parses user intent and determines required actions.
2. **Schema Agent:** Queries the target database's catalog/schema to fetch relevant tables, columns, and types.
3. **SQL Agent:** Formulates the SQL query based on the user's question and schema context.
4. **Analysis Agent:** Interprets SQL query outputs to generate natural language explanations and summaries.
5. **Visualization Agent:** Decides on the best visualization format (bar chart, line graph, scatter plot) and prepares data payloads.
6. **Report Agent:** Consolidates insights and builds downloadable PDF assets.

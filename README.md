# Agentic AI Portfolio – LangGraph Multi‑Agent System

A production‑ready multi‑agent system built with **LangGraph**, **LangSmith**, and **Ollama**.  
Implements a **priority‑based** multi‑agent flow (Legal → Budget → Location → Resolver) with tool integration, real‑world data (CSV), and legal veto logic. Designed to be extended with enterprise data sources and workflow automation.

## Architecture

[User Query] → [Legal Agent] → [Budget Agent] → [Location Agent] → [Resolver] → [Final Answer]
│ │ │ │
▼ ▼ ▼ ▼
legal_tool budget_tool location_tool priority logic
(CSV) (CSV) (CSV) (legal veto)

It visually maps the path from User Query through the agents (Legal, Budget, Location), into the Resolver, and finally down to the Final Answer with clear approval or veto outcomes.

- **ReAct reasoning** inside each specialist
- **Shared state** passed through LangGraph
- **Tool‑augmented** specialists using CSV data
- **Legal veto** overrides all other opinions
- **LangSmith tracing** for observability

## Features

- 100% local (Ollama) or cloud models
- Extensible data layer (CSV → API → database)
- Clean separation of tools, prompts, orchestration
- Ready to be wrapped in a FastAPI service and connected to n8n workflows

## Prerequisites

- Python 3.10+
- Ollama with `phi3:mini` (or any model)
- (Optional) LangSmith account for tracing

## Installation

```bash
git clone https://github.com/raj266/agentic-ai-portfolio.git
cd agentic-ai-portfolio
pip install -r requirements.txt

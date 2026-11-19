# chess-coach

A personal chess coach: RAG over open-licensed chess literature, plus an agent that reviews
the owner's games. It is a learning project and interview portfolio piece. The owner must be
able to explain every line, so understanding matters more than speed.

Current phase and step status are in [PLAN.md](PLAN.md). Read it before starting work and
update the checkboxes when a step is finished.

## How to work here

- Explain what we are about to do and why before writing code.
- One small step at a time. Do not build ahead or add features that were not asked for.
- Explain each new concept (LangChain object, embedding, retriever...) briefly in plain terms.
- Prefer simple, readable code over clever code. Use the framework where that is standard.
- End each step with: what the owner should be able to explain, and one small part they
  could write themselves.
- The owner knows basic git and uv; no need to explain those.
- The owner makes the commits.
- Do not start the next phase until the current one works and is understood.

## Stack rules

- Windows 11, PowerShell. Python 3.12, managed with uv (`uv add`, `uv run`, never pip).
- LangChain 1.x and LangGraph 1.x. Use current APIs (`init_chat_model`, `create_agent`).
  Never `AgentExecutor` or `langgraph.prebuilt`. Check the current docs when unsure.
- Models run locally through Ollama. Model names come from `src/chess_coach/config.py`
  only; never hard-code a model name anywhere else.
- Chroma for the vector store. python-chess and Stockfish from Phase 3 on.

## Layout

- `src/chess_coach/`: all importable code. `scripts/`: small runnable experiments.
- `data/` is git-ignored. `data/raw/` is never edited by hand or by code after download.
- The repo is public: open-licensed corpus only, every source listed in `SOURCES.md`,
  no secrets (real values go in `.env`, which is ignored).

## Commands

- `uv sync`: install everything from the lockfile.
- `uv run python scripts/<name>.py`: run an experiment script.
- `uv run pytest`: run the tests (once pytest is added).

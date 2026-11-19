# Plan

Phase 0 is fixed. Phases 1-5 are the intended route: the steps and their order are firm,
but details (exact libraries, sizes, numbers) get confirmed when each phase starts, because
what we measure in one phase decides what we do in the next.

## Overview

| Phase | Goal | You end up with |
|---|---|---|
| 0. Setup (in progress) | Tools work, one chat call, one embedding call | A project that runs and a first experiment |
| 1. Basic RAG | Answer chess questions from a small corpus, with citations | `chess-coach ask "..."` in the terminal |
| 2. Evaluation | Measure quality, improve one change at a time | A results table that justifies every design choice |
| 3. Tools + agent | One agent that can search, use the engine, read PGN | `chess-coach chat` that can look at a position |
| 4. Game review | A fixed multi-step workflow that reviews a whole game | `chess-coach review game.pgn` producing a checked review |
| 5. Polish | Make it presentable | UI, README, tests, demo |

## Decisions

- Package layout: `src/chess_coach/`.
- `data/` and the Chroma index are not committed; fetch scripts and `SOURCES.md` are.
- Code licence: MIT.
- pytest from Phase 0.
- LLM thinking mode: off in Phases 0-1, compared in Phase 2.
- Chat model: `qwen3.5:9b` (100% GPU at 4096 context, about 5.6 GB). Fallback `qwen3:8b`.
  Context length will be set explicitly in `config.py` and re-checked with `ollama ps`.
- Embeddings: `qwen3-embedding:0.6b`, with `nomic-embed-text` as comparison.
- Labels: two separate fields, used for both corpus metadata and mistake classification.
  `phase`: opening / middlegame / endgame / any. `category`: tactics / strategy / theory.

---

## Phase 0: Setup

- [x] 0.1 Repo hygiene: `.gitignore`, project description (first commit still to make)
- [x] 0.2 Package layout: `src/chess_coach/`, build system
- [ ] 0.3 Ollama models pulled and running on the GPU (chat model done; `nomic-embed-text` still to pull)
- [x] 0.4 Dependencies: `langchain`, `langchain-ollama`, `pytest` (dev)
- [ ] 0.5 `config.py`: model names and Ollama URL in one place
- [ ] 0.6 First chat call with `init_chat_model`
- [ ] 0.7 First embedding call and cosine similarity
- [ ] 0.8 Casing test ("Bb5" vs "bb5") on both embedding models, results in `docs/experiments.md`
- [ ] 0.9 README section, commit, explain each step back

**Done when:** both scripts run from a clean clone with `uv sync`, and the casing results are written down.

---

## Phase 1: Basic RAG

**Goal:** the simplest pipeline that works end to end. No tuning; Phase 2 is for that.

**New concepts:** document, metadata, chunk, vector store, retriever, top-k, prompt template, grounding, citation.

**New packages (expected):** `langchain-chroma`, `langchain-text-splitters`, `httpx` for downloads.

**Corpus for this phase:** deliberately small, about 15-25 Wikipedia articles (e.g. Fork, Pin,
Skewer, Italian Game, Sicilian Defence, Opposition, Lucena position, Pawn structure). Small
enough that you can read the chunks yourself and judge retrieval by eye.

- [ ] 1.1 **Pick the articles.** Write the list in a small file with two labels for each:
      `phase` (opening / middlegame / endgame / any) and `category` (tactics / strategy / theory).
      Check every phase and category has a few articles. *Learn:* corpus design is a decision, not
      a download.
- [ ] 1.2 **Fetch → `data/raw/`.** Download each article through the Wikipedia API and save it
      untouched, plus the URL and date. Start `SOURCES.md`. *Learn:* why raw data is never
      edited (you can always re-clean, never re-guess); what CC BY-SA attribution requires.
- [ ] 1.3 **Clean → `data/processed/`.** Turn each article into markdown with a metadata
      header (source, url, license, phase, category, notation). Drop references, navigation boxes,
      "See also". *Learn:* most RAG quality problems start here; what metadata is for.
- [ ] 1.4 **Chunk.** Split the markdown into pieces, by heading first, then by size with a
      small overlap. Print some chunks and read them. *Learn:* why we chunk at all (embedding
      and context limits, precision), size vs overlap trade-off, why a chunk must make sense alone.
- [ ] 1.5 **Embed + store in Chroma.** One command that rebuilds the index from
      `data/processed/`. *Learn:* what a vector store does, what is stored (vector + text +
      metadata), why the index is disposable and the processed files are not.
- [ ] 1.6 **Retrieve only.** A script that takes a question and prints the top-k chunks with
      scores, with no LLM involved. *Learn:* retrieval is a separate, testable stage; if the
      right chunk is not here, no prompt can fix the answer.
- [ ] 1.7 **Answer with citations.** Prompt = instructions + retrieved chunks (numbered) +
      question. The model must cite chunk numbers and say "I don't know" when the chunks don't
      cover it. *Learn:* prompt templates, grounding, why citations are produced from our
      metadata and not invented by the model.
- [ ] 1.8 **CLI.** `chess-coach ask "What is a fork?"` prints the answer and its sources.
      *Learn:* an entry point; keeping the pipeline in the package and the CLI thin.
- [ ] 1.9 **Try to break it.** Ask 10 questions including ones outside the corpus, write down
      what goes wrong. These notes become Phase 2's starting point.

**Done when:** it answers in-corpus questions with correct citations, refuses out-of-corpus
ones, and you can draw the pipeline from memory.

**Your-turn candidates:** the article list, the metadata header format, the wording of the answer prompt.

---

## Phase 2: Evaluation and improvement

**Goal:** replace "it seems better" with numbers, then improve one change at a time.

**New concepts:** golden dataset, hit rate, MRR, faithfulness, LLM-as-judge, baseline,
ablation, BM25, hybrid search, reciprocal rank fusion, reranker, metadata filter, tracing.

**New packages (expected):** `langsmith`; later `rank-bm25` and a reranker, chosen when we get there.

- [ ] 2.1 **Write the question set.** 30-50 questions you write, each with the verified answer
      and the article that contains it. Mix: easy facts, concepts, notation-heavy
      ("what is the idea behind 3.Bb5?"), and a few unanswerable ones. *Learn:* the eval set
      is the most valuable artefact in a RAG project; why you write it and not the LLM.
- [ ] 2.2 **Retrieval metrics.** Hit rate@k (is the right source in the top k?) and MRR (how
      high?). No LLM needed, so it is fast and deterministic. *Learn:* measuring retrieval
      separately from generation.
- [ ] 2.3 **Answer metrics.** Faithfulness (is every claim supported by the retrieved chunks?)
      and correctness (does it match your answer?), scored by an LLM judge. Hand-check a
      sample of the judge's verdicts. *Learn:* LLM-as-judge and its limits, especially with a
      small local judge.
- [ ] 2.4 **Baseline run.** Run the Phase 1 pipeline unchanged, record row 1 of
      `eval/results.md`. *Learn:* nothing can be called an improvement without a baseline.
- [ ] 2.5 **LangSmith tracing.** Turn tracing on and look at one full run: what was retrieved,
      the exact prompt, timings. *Learn:* reading a trace to find which stage failed.
- [ ] 2.6 **Experiments, one change each, each a new row in the table:**
  - [ ] a. Chunk size and overlap
  - [ ] b. Embedding model: `qwen3-embedding` vs `nomic-embed-text` (uses the Phase 0 casing result)
  - [ ] c. Hybrid search: BM25 keyword search + vector search, fused. Expected to help on
        exact notation like "Bb5", where embeddings are weak
  - [ ] d. Reranker on the top results
  - [ ] e. Metadata filters (phase, category, ECO code)
  - [ ] f. LLM: thinking on vs off, and model size
- [ ] 2.7 **Grow the corpus.** Add Wikibooks, a Gutenberg book (Capablanca, including the
      descriptive-notation handling), and the Lichess openings dataset as metadata. Re-run the
      eval. *Learn:* how results change with scale and messier sources; converting
      "P-K4" to "e4" as a cleaning step.
- [ ] 2.8 **Choose the final configuration** and write two paragraphs on why.

**Done when:** `eval/results.md` has a baseline and at least five experiment rows, and the
chosen configuration is justified by the table.

**Your-turn candidates:** all the questions (2.1), the hit-rate function, the reciprocal rank fusion function (about 10 lines).

---

## Phase 3: Tools and a single agent

**Goal:** go from a fixed pipeline to a model that decides which tool to call.

**New concepts:** tool, tool calling, tool schema and docstring, the agent loop
(model → tool → model), system prompt, FEN, PGN, centipawn evaluation, UCI.

**New packages (expected):** `chess` (python-chess). Stockfish is installed separately as a program.

- [ ] 3.1 **python-chess basics, no LLM.** Load a position from FEN, list legal moves, play a
      move, read a PGN file. *Learn:* the chess library is the source of truth; the LLM is not.
- [ ] 3.2 **Stockfish.** Install it, talk to it through python-chess, get an evaluation and
      best move for a position. *Learn:* what an engine evaluation means, depth vs time limits.
- [ ] 3.3 **First tool: `legal_moves`.** Wrap the function with `@tool`, call it by hand, look
      at the schema the model will see. *Learn:* a tool is a function plus a description; the
      description is prompt engineering.
- [ ] 3.4 **`engine_eval` and `load_game` tools.** Same pattern. *Learn:* designing tool inputs
      and outputs a small model can use reliably (short, structured, clear errors).
- [ ] 3.5 **`search_knowledge` tool.** The Phase 2 retriever wrapped as a tool, returning
      chunks with their sources. *Learn:* "RAG as a tool" versus "RAG as a pipeline".
- [ ] 3.6 **The agent.** `create_agent` with the model, the four tools and a system prompt.
      Read the trace of one run in LangSmith, step by step. *Learn:* the agent loop, when the
      model stops, what the message history looks like.
- [ ] 3.7 **Failure cases.** Wrong tool, invented arguments, loops, ignoring tool results.
      Fix with better tool descriptions and limits. *Learn:* small local models are weak at
      tool calling; where an agent is the wrong choice.
- [ ] 3.8 **CLI.** `chess-coach chat` with conversation memory for the session.

**Done when:** given a FEN and "what should I play and why?", the agent calls the engine,
looks up the concept, and answers with a legal move and a citation.

**Your-turn candidates:** the `legal_moves` tool, one tool description, a pytest test for a tool.

---

## Phase 4: Game-review workflow (LangGraph)

**Goal:** review a full game with a fixed, inspectable workflow, and catch hallucinated moves.

**Why not just the Phase 3 agent:** a game review is the same steps every time. A graph makes
the order explicit, each step testable, and lets us add a validation loop. Knowing when to use
an agent and when to use a workflow is a common interview question.

**New concepts:** state, node, edge, conditional edge, cycle, checkpointer, thread,
resume, human-in-the-loop.

**New packages (expected):** `langgraph` (already installed with langchain), a SQLite checkpointer.

- [ ] 4.1 **Design on paper.** Draw the graph and define the state (the data passed between
      steps) before any code. *Learn:* state design is the main design decision in LangGraph.
- [ ] 4.2 **Two-node graph.** Load PGN → run the engine over every move. No LLM. *Learn:*
      `StateGraph`, nodes as plain functions, how state updates merge.
- [ ] 4.3 **Find critical moments.** Pick the moves where the evaluation dropped most, and
      label each with its `phase` from the move number and material left (plain Python).
      *Learn:* keeping deterministic work out of the LLM.
- [ ] 4.4 **Classify each mistake by `category`** (tactics / strategy / theory), with structured
      output. *Learn:* structured output with a schema instead of parsing free text.
- [ ] 4.5 **Retrieve the concept** for each mistake using the Phase 2 retriever, filtered by
      the mistake's `phase` and `category`. *Learn:* why shared labels connect the agent to the RAG.
- [ ] 4.6 **Write the review.** One LLM node that gets the moments, engine lines and concepts.
- [ ] 4.7 **Validator node.** Extract every move the review mentions and check it with
      python-chess against the real position. If any are illegal, loop back to the writer
      with the errors, up to a retry limit. *Learn:* conditional edges and cycles; verifying
      LLM output with code. This is the part to highlight given your security background.
- [ ] 4.8 **Checkpointing.** Save state after each node, kill a run midway, resume it.
      *Learn:* what a checkpointer stores, threads, why this matters for long runs.
- [ ] 4.9 **CLI and measurement.** `chess-coach review game.pgn`. Run it on about 10 of your
      games and record how often the validator catches something.

**Done when:** it reviews one of your real games, every move in the review is legal, and you
can show a run where the validator caught and fixed a hallucination.

**Your-turn candidates:** the state definition, the critical-moment function, the retry condition.

---

## Phase 5: Polish

**Goal:** someone who opens the repo understands it in two minutes and can run it.

- [ ] 5.1 **Streamlit UI.** Two tabs: ask a question, review a game (with a board). A thin
      layer over the package, no logic of its own.
- [ ] 5.2 **Tests.** Cleaning, chunking, metrics, tools, validator. Nothing that needs a model
      to be running. *Learn:* what is worth testing in an LLM app and what is covered by evals instead.
- [ ] 5.3 **README.** What it is, architecture diagram, the eval table, how to run, limitations.
- [ ] 5.4 **Licences.** `LICENSE` (MIT), `SOURCES.md` complete and checked.
- [ ] 5.5 **Clean-clone test.** Follow your own README on a fresh clone.
- [ ] 5.6 **Demo.** Short recording or GIF, plus a two-minute spoken walkthrough you practise.
- [ ] 5.7 **Interview notes.** One page: the three decisions you would defend, the three
      things you would do differently, what would change in production (hosted models,
      scale, cost, security such as prompt injection through the corpus).

**Done when:** the clean-clone test passes and you can give the walkthrough without notes.

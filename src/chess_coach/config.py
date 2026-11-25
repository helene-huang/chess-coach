"""Project settings, all in one place.

Each setting has a default below. To change one on your machine, put it in a
.env file at the project root (see .env.example). No other file should
hard-code a model name or URL: import it from here instead.
"""

import os

from dotenv import load_dotenv

# Copy the lines of .env (if the file exists) into the environment variables.
# A variable already set in the terminal wins over the file.
load_dotenv()

# Chat model that writes the answers.
CHAT_MODEL = os.getenv("CHAT_MODEL", "qwen3.5:9b")

# Embedding model that turns text into vectors.
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "qwen3-embedding:0.6b")

# Address of the local Ollama server.
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")

# Context window in tokens: prompt + thinking + answer must all fit.
# Ollama's default (4096) is too small for RAG prompts.
NUM_CTX = int(os.getenv("NUM_CTX", "8192"))

# Whether the chat model thinks before answering. Off for Phases 0-1.
THINKING = os.getenv("THINKING", "false").lower() == "true"

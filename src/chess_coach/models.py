"""Build the models the project uses, from the settings in config.py.

Every script and module gets its model from here, so they all use the same
model name, server address and options.
"""

from langchain.chat_models import init_chat_model

from chess_coach import config


def get_chat_model():
    """Return the chat model described in config.py, served by Ollama."""
    return init_chat_model(
        config.CHAT_MODEL,
        model_provider="ollama",
        base_url=config.OLLAMA_BASE_URL,
        num_ctx=config.NUM_CTX,
        reasoning=config.THINKING,
    )

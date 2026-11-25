"""Step 0.6: send one question to the chat model and look at what comes back.

Run with:  uv run python scripts/hello_chat.py
"""

from langchain.messages import HumanMessage, SystemMessage

from chess_coach import config
from chess_coach.models import get_chat_model

model = get_chat_model()

messages = [
    SystemMessage("You are a chess coach for a beginner. Answer in two or three sentences."),
    HumanMessage("What is a fork in chess?"),
]

reply = model.invoke(messages)

print(f"Model: {config.CHAT_MODEL} (thinking: {config.THINKING}, context: {config.NUM_CTX})")
print()
print("Answer:")
print(reply.content)
print()
print("Reply type:", type(reply).__name__)
print("Tokens used:", reply.usage_metadata)

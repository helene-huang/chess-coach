"""Chat with the model in the terminal, with follow-up questions.

The model remembers nothing between calls, so every turn sends the whole
conversation so far. When you stop, the conversation is added to
docs/llm-log.md for you to review.

Run with:  uv run python scripts/chat.py
Press Enter on an empty line to stop.
"""

from langchain.messages import HumanMessage, SystemMessage

from chess_coach import config
from chess_coach.llm_log import log_conversation
from chess_coach.models import get_chat_model

SYSTEM_PROMPT = "You are a chess coach for a beginner. Answer in two or three sentences."

model = get_chat_model()
messages = [SystemMessage(SYSTEM_PROMPT)]
turns = []  # (question, answer) pairs, for the log

print(f"Model: {config.CHAT_MODEL} (thinking: {config.THINKING}, context: {config.NUM_CTX})")
print("Ask a question. Press Enter on an empty line to stop.")

while True:
    question = input("\nYou: ").strip()
    if not question:
        break

    messages.append(HumanMessage(question))
    reply = model.invoke(messages)
    messages.append(reply)  # so the next turn includes this answer

    print(f"\nCoach: {reply.content}")
    print(f"(tokens: {reply.usage_metadata['input_tokens']} in, "
          f"{reply.usage_metadata['output_tokens']} out)")
    turns.append((question, reply.content))

if turns:
    log_conversation(SYSTEM_PROMPT, turns)
    print(f"\nSaved {len(turns)} turn(s) to {config.LLM_LOG_PATH}")

"""Save chat conversations to docs/llm-log.md so each answer can be judged by hand.

Each entry records the settings and the system prompt, then every question and
answer, with a Verdict and a Comment line after each answer to fill in later.
"""

from datetime import datetime

from chess_coach import config


def log_conversation(system_prompt: str, turns: list[tuple[str, str]]) -> None:
    """Append one conversation to the log. `turns` is a list of (question, answer) pairs."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    thinking = "on" if config.THINKING else "off"

    lines = [
        f"## {timestamp} · {config.CHAT_MODEL} · thinking {thinking} · context {config.NUM_CTX}",
        "",
        f"**System:** {system_prompt}",
        "",
    ]
    for number, (question, answer) in enumerate(turns, start=1):
        lines += [
            f"**Q{number}:** {question}",
            "",
            f"**A{number}:** {answer}",
            "",
            f"**Verdict A{number}:** TODO (correct / partly wrong / mostly wrong / wrong)",
            "",
            f"**Comment A{number}:** TODO",
            "",
        ]
    lines.append("")

    with config.LLM_LOG_PATH.open("a", encoding="utf-8") as log_file:
        log_file.write("\n".join(lines))

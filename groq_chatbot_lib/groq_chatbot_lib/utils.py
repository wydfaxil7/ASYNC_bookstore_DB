from typing import Optional


def format_history(history: list, show_system: bool = False) -> str:
    if not history:
        return "[No conversation history]"

    output = []
    for turn in history:
        role = turn.get("role", "unknown")
        content = turn.get("content", "")

        if role == "system" and not show_system:
            continue

        label = role.upper()
        output.append(f"[{label}]: {content}")

    if not output:
        return "[No valid messages in history]"

    return "\n".join(output)


def count_tokens_estimate(text: str) -> int:
    if not text or not isinstance(text, str):
        return 0
    return max(1, len(text) // 4)


def is_within_token_limit(text: str, limit: int) -> bool:
    if limit < 1:
        raise ValueError("limit must be at least 1")
    return count_tokens_estimate(text) <= limit


def history_to_text(history: list, show_system: bool = False) -> str:
    if not history:
        return ""

    lines = []
    for turn in history:
        role = turn.get("role", "unknown")
        content = turn.get("content", "")

        if role == "system" and not show_system:
            continue

        if role == "user":
            lines.append(f"User: {content}")
        elif role == "assistant":
            lines.append(f"Assistant: {content}")
        elif role == "system":
            lines.append(f"System: {content}")

    return "\n".join(lines)


def estimate_history_tokens(history: list) -> int:
    if not history:
        return 0

    total_text = " ".join(
        turn.get("content", "")
        for turn in history
    )
    return count_tokens_estimate(total_text)


def split_text_into_chunks(text: str, max_tokens: int = 500) -> list[str]:
    if not text or not isinstance(text, str):
        return []

    max_chars = max_tokens * 4
    words = text.split()
    chunks = []
    current_chunk = []
    current_length = 0

    for word in words:
        word_length = len(word) + 1

        if current_length + word_length > max_chars and current_chunk:
            chunks.append(" ".join(current_chunk))
            current_chunk = [word]
            current_length = word_length
        else:
            current_chunk.append(word)
            current_length += word_length

    if current_chunk:
        chunks.append(" ".join(current_chunk))

    return chunks


def sanitize_message(text: str, max_length: int = 2000) -> str:
    if not text or not isinstance(text, str):
        raise ValueError("Message cannot be empty")

    cleaned = text.replace("\x00", "").strip()
    cleaned = " ".join(cleaned.split())

    if not cleaned:
        raise ValueError("Message cannot be empty after cleaning")

    if len(cleaned) > max_length:
        cleaned = cleaned[:max_length]

    return cleaned
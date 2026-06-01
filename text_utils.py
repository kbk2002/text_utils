"""
text_utils.py – A small text-processing utility library.

Functions
---------
word_count(text)            – count words in a string
char_frequency(text)        – letter frequency map (case-insensitive, letters only)
is_palindrome(text)         – True if the string reads the same forwards and backwards
caesar_cipher(text, shift)  – ROT-n encode/decode
truncate(text, max_len, suffix) – shorten long strings with an ellipsis (or custom suffix)
count_lines(filepath)       – count non-empty lines in a file (I/O integration point)
most_common_words(text, n)  – return the n most-frequent words
"""

from __future__ import annotations

import re
from collections import Counter
from pathlib import Path


# ---------------------------------------------------------------------------
# Pure / in-memory helpers
# ---------------------------------------------------------------------------

def word_count(text: str) -> int:
    """Return the number of whitespace-delimited tokens in *text*."""
    if not isinstance(text, str):
        raise TypeError(f"Expected str, got {type(text).__name__}")
    return len(text.split())


def char_frequency(text: str) -> dict[str, int]:
    """Return a dict mapping each letter (lower-cased) to its occurrence count.

    Non-alphabetic characters are ignored.
    """
    if not isinstance(text, str):
        raise TypeError(f"Expected str, got {type(text).__name__}")
    freq: dict[str, int] = {}
    for ch in text.lower():
        if ch.isalpha():
            freq[ch] = freq.get(ch, 0) + 1
    return freq


def is_palindrome(text: str) -> bool:
    """Return True if *text* (ignoring case, spaces, and punctuation) is a palindrome."""
    if not isinstance(text, str):
        raise TypeError(f"Expected str, got {type(text).__name__}")
    cleaned = re.sub(r"[^a-z0-9]", "", text.lower())
    return cleaned == cleaned[::-1]


def caesar_cipher(text: str, shift: int) -> str:
    """Encode *text* with a Caesar cipher of *shift* positions.

    Non-alpha characters are passed through unchanged.
    Use a negative *shift* (or ``shift = 26 - n``) to decode.
    """
    if not isinstance(text, str):
        raise TypeError(f"Expected str, got {type(text).__name__}")
    if not isinstance(shift, int):
        raise TypeError(f"shift must be int, got {type(shift).__name__}")

    result = []
    shift = shift % 26  # normalise
    for ch in text:
        if ch.isalpha():
            base = ord("A") if ch.isupper() else ord("a")
            result.append(chr((ord(ch) - base + shift) % 26 + base))
        else:
            result.append(ch)
    return "".join(result)


def truncate(text: str, max_len: int, suffix: str = "...") -> str:
    """Return *text* truncated to *max_len* characters (including *suffix*).

    If ``len(text) <= max_len`` the original string is returned unchanged.
    """
    if not isinstance(text, str):
        raise TypeError(f"Expected str, got {type(text).__name__}")
    if max_len < len(suffix):
        raise ValueError(
            f"max_len ({max_len}) must be >= len(suffix) ({len(suffix)})"
        )
    if len(text) <= max_len:
        return text
    return text[: max_len - len(suffix)] + suffix


def most_common_words(text: str, n: int = 5) -> list[tuple[str, int]]:
    """Return the *n* most frequent words as ``[(word, count), …]`` (descending).

    Words are lower-cased; punctuation attached to words is stripped.
    """
    if not isinstance(text, str):
        raise TypeError(f"Expected str, got {type(text).__name__}")
    if n < 0:
        raise ValueError("n must be >= 0")
    words = re.findall(r"[a-z]+", text.lower())
    return Counter(words).most_common(n)


# ---------------------------------------------------------------------------
# I/O helper (integration point)
# ---------------------------------------------------------------------------

def count_lines(filepath: str | Path) -> int:
    """Return the number of non-empty lines in *filepath*.

    Raises ``FileNotFoundError`` if the file does not exist.
    """
    path = Path(filepath)
    if not path.exists():
        raise FileNotFoundError(f"No such file: {filepath}")
    with path.open("r", encoding="utf-8") as fh:
        return sum(1 for line in fh if line.strip())

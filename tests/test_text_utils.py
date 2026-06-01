"""
tests/test_text_utils.py – Unit and integration tests for text_utils.py

Run with:
    pytest -v --tb=short --cov=text_utils --cov-report=term-missing
"""

from __future__ import annotations

import os
import sys
import tempfile
from pathlib import Path

import pytest

# Make sure the project root is on sys.path when running from any CWD
sys.path.insert(0, str(Path(__file__).parent.parent))

from text_utils import (
    caesar_cipher,
    char_frequency,
    count_lines,
    is_palindrome,
    most_common_words,
    truncate,
    word_count,
)


# ===========================================================================
# word_count
# ===========================================================================

class TestWordCount:
    def test_simple_sentence(self):
        assert word_count("hello world") == 2

    def test_single_word(self):
        assert word_count("pytest") == 1

    def test_empty_string(self):
        assert word_count("") == 0

    def test_extra_whitespace(self):
        assert word_count("  lots   of   spaces  ") == 3

    def test_newlines_and_tabs(self):
        assert word_count("line1\nline2\ttab") == 3

    def test_type_error(self):
        with pytest.raises(TypeError):
            word_count(42)  # type: ignore[arg-type]

    def test_numbers_as_words(self):
        assert word_count("1 2 3") == 3


# ===========================================================================
# char_frequency
# ===========================================================================

class TestCharFrequency:
    def test_basic(self):
        freq = char_frequency("aAbB")
        assert freq == {"a": 2, "b": 2}

    def test_ignores_non_alpha(self):
        freq = char_frequency("hello, world! 123")
        assert "," not in freq
        assert "1" not in freq
        assert " " not in freq

    def test_empty_string(self):
        assert char_frequency("") == {}

    def test_only_punctuation(self):
        assert char_frequency("!@#$%") == {}

    def test_case_insensitive(self):
        freq = char_frequency("AaAa")
        assert freq == {"a": 4}

    def test_type_error(self):
        with pytest.raises(TypeError):
            char_frequency(None)  # type: ignore[arg-type]

    def test_unicode_letters(self):
        # Non-ASCII letters are still alpha in Python
        freq = char_frequency("café")
        assert "c" in freq and "a" in freq


# ===========================================================================
# is_palindrome
# ===========================================================================

class TestIsPalindrome:
    def test_simple_palindrome(self):
        assert is_palindrome("racecar") is True

    def test_not_palindrome(self):
        assert is_palindrome("hello") is False

    def test_with_spaces(self):
        assert is_palindrome("A man a plan a canal Panama") is True

    def test_with_punctuation(self):
        assert is_palindrome("Was it a car or a cat I saw?") is True

    def test_empty_string(self):
        assert is_palindrome("") is True

    def test_single_character(self):
        assert is_palindrome("x") is True

    def test_mixed_case(self):
        assert is_palindrome("Madam") is True

    def test_numeric_palindrome(self):
        assert is_palindrome("12321") is True

    def test_type_error(self):
        with pytest.raises(TypeError):
            is_palindrome(["r", "a", "c", "e"])  # type: ignore[arg-type]


# ===========================================================================
# caesar_cipher
# ===========================================================================

class TestCaesarCipher:
    def test_basic_encode(self):
        assert caesar_cipher("abc", 1) == "bcd"

    def test_wrap_around_lower(self):
        assert caesar_cipher("xyz", 3) == "abc"

    def test_wrap_around_upper(self):
        assert caesar_cipher("XYZ", 3) == "ABC"

    def test_preserves_non_alpha(self):
        assert caesar_cipher("Hello, World!", 0) == "Hello, World!"

    def test_zero_shift(self):
        assert caesar_cipher("Python", 0) == "Python"

    def test_full_round_trip(self):
        original = "The quick brown fox"
        encoded = caesar_cipher(original, 13)
        decoded = caesar_cipher(encoded, -13)
        assert decoded == original

    def test_rot13_self_inverse(self):
        msg = "Hello World"
        assert caesar_cipher(caesar_cipher(msg, 13), 13) == msg

    def test_large_shift_normalised(self):
        # shift of 27 is the same as shift of 1
        assert caesar_cipher("a", 27) == caesar_cipher("a", 1)

    def test_negative_shift(self):
        assert caesar_cipher("bcd", -1) == "abc"

    def test_type_error_text(self):
        with pytest.raises(TypeError):
            caesar_cipher(123, 1)  # type: ignore[arg-type]

    def test_type_error_shift(self):
        with pytest.raises(TypeError):
            caesar_cipher("hi", "3")  # type: ignore[arg-type]


# ===========================================================================
# truncate
# ===========================================================================

class TestTruncate:
    def test_no_truncation_needed(self):
        assert truncate("hello", 10) == "hello"

    def test_exact_length(self):
        assert truncate("hello", 5) == "hello"

    def test_truncation_with_default_suffix(self):
        result = truncate("hello world", 8)
        assert result == "hello..."
        assert len(result) == 8

    def test_custom_suffix(self):
        result = truncate("hello world", 7, suffix="--")
        assert result.endswith("--")
        assert len(result) == 7

    def test_empty_suffix(self):
        result = truncate("hello world", 5, suffix="")
        assert result == "hello"

    def test_empty_string(self):
        assert truncate("", 5) == ""

    def test_max_len_equals_suffix_length(self):
        result = truncate("hello", 3, suffix="...")
        assert result == "..."

    def test_max_len_less_than_suffix_raises(self):
        with pytest.raises(ValueError):
            truncate("hello", 2, suffix="...")

    def test_type_error(self):
        with pytest.raises(TypeError):
            truncate(42, 5)  # type: ignore[arg-type]


# ===========================================================================
# most_common_words
# ===========================================================================

class TestMostCommonWords:
    SAMPLE = "the cat sat on the mat the cat"

    def test_top_1(self):
        result = most_common_words(self.SAMPLE, 1)
        assert result[0] == ("the", 3)

    def test_top_2(self):
        result = most_common_words(self.SAMPLE, 2)
        assert result[0][0] == "the"
        assert result[1][0] == "cat"

    def test_default_n(self):
        long_text = " ".join(["word"] * 10 + ["other"] * 5 + ["more"] * 3)
        result = most_common_words(long_text)
        assert len(result) <= 5

    def test_empty_string(self):
        assert most_common_words("") == []

    def test_n_zero(self):
        assert most_common_words(self.SAMPLE, 0) == []

    def test_negative_n_raises(self):
        with pytest.raises(ValueError):
            most_common_words(self.SAMPLE, -1)

    def test_punctuation_stripped(self):
        result = most_common_words("hello, hello! hello.")
        assert result[0] == ("hello", 3)

    def test_case_insensitive(self):
        result = most_common_words("The the THE")
        assert result[0] == ("the", 3)

    def test_type_error(self):
        with pytest.raises(TypeError):
            most_common_words(None)  # type: ignore[arg-type]


# ===========================================================================
# count_lines  (integration tests – touches the real filesystem)
# ===========================================================================

class TestCountLines:
    """Integration tests: write real temporary files, then call count_lines."""

    def test_normal_file(self, tmp_path):
        p = tmp_path / "sample.txt"
        p.write_text("line one\nline two\nline three\n", encoding="utf-8")
        assert count_lines(p) == 3

    def test_empty_lines_not_counted(self, tmp_path):
        p = tmp_path / "gaps.txt"
        p.write_text("first\n\n\nsecond\n\n", encoding="utf-8")
        assert count_lines(p) == 2

    def test_single_line_no_newline(self, tmp_path):
        p = tmp_path / "single.txt"
        p.write_text("just one line", encoding="utf-8")
        assert count_lines(p) == 1

    def test_all_blank_lines(self, tmp_path):
        p = tmp_path / "blank.txt"
        p.write_text("\n\n\n", encoding="utf-8")
        assert count_lines(p) == 0

    def test_empty_file(self, tmp_path):
        p = tmp_path / "empty.txt"
        p.write_text("", encoding="utf-8")
        assert count_lines(p) == 0

    def test_file_not_found(self, tmp_path):
        with pytest.raises(FileNotFoundError):
            count_lines(tmp_path / "nonexistent.txt")

    def test_accepts_string_path(self, tmp_path):
        p = tmp_path / "str_path.txt"
        p.write_text("a\nb\nc\n", encoding="utf-8")
        assert count_lines(str(p)) == 3

    def test_integration_with_word_count(self, tmp_path):
        """Integration: write lines, read them back, and verify word counts."""
        lines = ["the quick brown fox", "jumped over the lazy dog", "hello world"]
        p = tmp_path / "words.txt"
        p.write_text("\n".join(lines), encoding="utf-8")

        assert count_lines(p) == len(lines)

        # "the quick brown fox" = 4, "jumped over the lazy dog" = 5, "hello world" = 2
        total_words = sum(word_count(line) for line in lines)
        assert total_words == 11

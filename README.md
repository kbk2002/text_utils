# text-utils

A small, well-tested Python text-processing utility library.

## Functions

| Function | Description |
|---|---|
| `word_count(text)` | Count whitespace-delimited words |
| `char_frequency(text)` | Letter-frequency map (case-insensitive, letters only) |
| `is_palindrome(text)` | True if the string is a palindrome (ignores case/punctuation) |
| `caesar_cipher(text, shift)` | ROT-n encode / decode |
| `truncate(text, max_len, suffix)` | Shorten long strings with a custom suffix |
| `most_common_words(text, n)` | Top-n most frequent words |
| `count_lines(filepath)` | Count non-empty lines in a file |

---

## Quick start

### 1 · Clone the repo

```bash
git clone https://github.com/<your-username>/text-utils.git
cd text-utils
```

### 2 · Create a virtual environment (optional but recommended)

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
```

### 3 · Install test dependencies

```bash
pip install -r requirements-dev.txt
```

---

## Running the tests

### Basic run (verbose)

```bash
pytest
```

`pyproject.toml` already sets `addopts = "-v --tb=short"` and `testpaths = ["tests"]`,
so this is all you need.

### With coverage report

```bash
pytest --cov=text_utils --cov-report=term-missing
```

### With HTML coverage report

```bash
pytest --cov=text_utils --cov-report=html
open htmlcov/index.html          # macOS
xdg-open htmlcov/index.html      # Linux
start htmlcov/index.html         # Windows
```

### Run a single test class

```bash
pytest tests/test_text_utils.py::TestCaesarCipher -v
```

---

## Test summary

| Class | Tests | What's covered |
|---|---|---|
| `TestWordCount` | 7 | Normal, empty, whitespace variants, type errors |
| `TestCharFrequency` | 7 | Case folding, non-alpha, unicode, type errors |
| `TestIsPalindrome` | 9 | Spaces, punctuation, numbers, mixed case |
| `TestCaesarCipher` | 11 | Wrap-around, round-trips, ROT-13, negative shift |
| `TestTruncate` | 9 | Exact length, custom suffix, edge lengths |
| `TestMostCommonWords` | 9 | Top-n, empty input, punctuation, type errors |
| `TestCountLines` *(integration)* | 8 | Real filesystem: blank lines, missing files, cross-function |

**Coverage: 100 % statements, 100 % branches** (`text_utils.py`).

---

## Project layout

```
text-utils/
├── text_utils.py          # utility library
├── tests/
│   ├── __init__.py
│   └── test_text_utils.py # full test suite (60 tests)
├── pyproject.toml         # pytest + coverage config
├── requirements-dev.txt   # pytest, pytest-cov
└── README.md
```

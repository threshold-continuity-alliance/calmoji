# 🧿 Contributing to Calmoji

Welcome to **Calmoji** — a symbolic scheduling engine built for coherence, ritual planning, and neurosemantic alignment.

This project blends **calendar logic**, **emoji glyphs**, and **semantic time structure** into a cohesive toolkit for personal and collective ritual coordination. We aim to keep the codebase clean, testable, and meaningful.

Below is a structured roadmap of planned enhancements and contributions, organized for clarity and triage.  
If you'd like to contribute, please read on. ✨

---

## 🔧 Roadmap: Code Enhancements & Features

### 🎛️ Configuration & CLI Improvements

- [ ] Add `--calendar-mode` flag (academic vs Gregorian logic)
- [ ] Add `--version` flag that reads from `__version__`
- [ ] Add `--output-dir` argument (default: `output/`)
- [ ] Add `--dry-run`, `--per-phase`, `--combined` options
- [ ] Load config from `~/.calmoji.yml` or CLI args (YAML/TOML support)
- [ ] Symbolic summary stats at end of runs

### 🧼 Code Quality & Structure

- [ ] Replace all `print()` calls with structured `logging`
- [ ] Remove duplicate imports and dead code
- [ ] Fix hardcoded year in `config.py`
- [ ] Add `__init__.py` in relevant folders
- [ ] Type hint return values consistently
- [ ] Add docstrings to all public functions and classes

### 🧠 Performance & Resilience

- [ ] Cache `EBI48_CLOCK` lookups
- [ ] Handle large year ranges with memory limits
- [ ] Sanitize all file paths
- [ ] Use atomic writes (tmp file + rename)
- [ ] Add progress indicator for long runs
- [ ] Benchmark large-output scenarios

---

## 🛡️ Error Handling & Validation

### 📁 File I/O

- [ ] Wrap file writes/reads in try-except
- [ ] Graceful degradation on missing permissions
- [ ] Handle disk full errors
- [ ] Unicode encoding errors → fallback logic or warnings

### 📅 Calendar Logic

- [ ] Validate input year (1900–2100)
- [ ] Ensure leap year behavior is consistent
- [ ] Handle DST transitions gracefully
- [ ] Catch invalid recurrence rule configs
- [ ] Add bounds checking for phase offset math
- [ ] Add protection against overlapping/malformed phases

### 🧩 Emoji & Encoding

- [ ] Validate emoji presence in `EBI48_CLOCK`
- [ ] Graceful fallback if emoji slot lookup fails
- [ ] Unicode validation at each ICS generation point

---

## 🧪 Unit Tests Under Development

### 🧹 Utility Functions

- [x] `slugify()` (unicode, punctuation, emoji edge cases)
- [ ] `generate_uid()` (determinism and entropy range)
- [ ] `get_emoji_for_time()` (boundaries, missing emoji)
- [ ] `create_ics_header()` (comment edge cases)
- [ ] `format_datetime()` line-folding & RFC conformance
- [ ] `group_phase_days_by_week()` edge spans (cross-year)

### 🧱 Structural Logic

- [ ] Phase boundaries with negative or offset edge cases
- [ ] Leap year tests (2024, 2028)
- [ ] ISO week crossovers (Dec/Jan weeks)
- [ ] Focus block generation for empty and full weeks

### 🧨 Error & Resilience Tests

- [ ] File permission denied during write
- [ ] Invalid emoji fallback
- [ ] Overlapping phase date logic
- [ ] Corrupt or unreadable config file

---

## 🧪 Integration & CLI Tests

- [ ] Full CLI pipeline test: all args, dry-run, combined
- [ ] `--calendar-mode` behavioral switch test
- [ ] Keyboard interrupt handling test (graceful exit)
- [ ] Unicode ics import tests (Apple/Outlook/Google Calendar)
- [ ] ICS RFC 5545 compliance check (line folding, encoding)

---

## 🧰 Developer Tooling

- [x] GitHub Actions CI (`ci.yml`)
- [x] Codecov badge and upload
- [ ] Add `black` and `ruff` linting
- [ ] Add `mypy` static typing check
- [ ] Add pre-commit hooks
- [ ] Set up `dependabot.yml` for Python dependencies

---

## 🏷️  Badges

```markdown
[![Calmoji CI](https://github.com/threshold-continuity-alliance/calmoji/actions/workflows/ci.yml/badge.svg?style=flat-square)](https://github.com/threshold-continuity-alliance/calmoji/actions/workflows/ci.yml)
[![codecov](https://codecov.io/gh/threshold-continuity-alliance/calmoji/branch/main/graph/badge.svg?style=flat-square)](https://codecov.io/gh/threshold-continuity-alliance/calmoji)

# 🧿 Contributing to Calmoji

Welcome to **Calmoji** — a symbolic scheduling engine built for coherence, ritual planning, and neurosemantic alignment.

This project blends **calendar logic**, **emoji glyphs**, and **semantic time structure** into a cohesive toolkit for personal and collective ritual coordination.
We aim to keep the codebase clean, testable, and meaningful.

If you're here to contribute — thank you.
Below is a structured roadmap of planned enhancements, organized for clarity and triage.

---

## 🔧 Roadmap: Code Enhancements & Features

### 🎛️ Configuration & CLI

* [ ] Add `--calendar-mode` flag (`academic` vs `gregorian`)
* [ ] Add `--version` flag (reads from `__version__`)
* [ ] Add `--output-dir` argument (default: `output/`)
* [ ] Add `--dry-run`, `--per-phase`, and `--combined` flags
* [ ] Support config loading from `~/.calmoji.yml` (YAML/TOML)
* [ ] Emit symbolic summary stats at end of run

### 🧼 Code Quality & Structure

* [ ] Replace all `print()` calls with structured `logging`
* [ ] Remove duplicate imports and dead code
* [ ] Fix hardcoded year in `config.py`
* [ ] Add `__init__.py` to module directories
* [ ] Add return type hints to all functions
* [ ] Add consistent docstrings to all public APIs

### 🧠 Performance & Resilience

* [ ] Cache `EBI48_CLOCK` lookups for speed
* [ ] Add memory protection for large year ranges
* [ ] Sanitize all file paths
* [ ] Implement atomic writes (temp file + rename)
* [ ] Add progress indicators for long ops
* [ ] Add optional runtime benchmarks for profiling

---

## 🛡️ Error Handling & Validation

### 📁 File I/O

* [ ] Wrap all I/O in `try-except` with friendly errors
* [ ] Fallback for permission-denied or disk-full conditions
* [ ] Handle unicode encoding failures cleanly
* [ ] Validate output directory existence and writability

### 📅 Calendar Logic

* [ ] Validate input year (1900–2100)
* [ ] Confirm leap year and ISO week rollover correctness
* [ ] Gracefully handle DST transitions
* [ ] Validate recurrence rules if present
* [ ] Guard against overlapping or malformed phase spans
* [ ] Add bounds-checking for phase math

### 🧩 Emoji & Encoding

* [ ] Validate presence of emoji in `EBI48_CLOCK`
* [ ] Fallback logic for missing or invalid glyphs
* [ ] Ensure UTF-8 validity at all export stages

---

## 🧪 Unit Tests Under Development

### 🧹 Utility Functions

* [x] `slugify()` — unicode, punctuation, emoji cases
* [ ] `generate_uid()` — uniqueness, entropy range
* [ ] `get_emoji_for_time()` — bounds and default fallback
* [ ] `create_ics_header()` — comment injection edge cases
* [ ] `format_datetime()` — RFC folding and boundaries
* [ ] `group_phase_days_by_week()` — multi-year and DST spans

### 🧱 Structural Logic

* [ ] Phase boundary edges (negatives, overlaps, empties)
* [ ] Leap year logic (2024, 2028)
* [ ] ISO week rollover (Dec/Jan)
* [ ] Focus block logic for full, empty, or partial weeks

### 🧨 Error & Resilience Tests

* [ ] Simulated file write failure
* [ ] Invalid emoji or clock mapping
* [ ] Corrupt config file handling
* [ ] Invalid CLI inputs and argument parsing

---

## 🧪 Integration & CLI Tests

* [ ] Full CLI test suite: dry-run, output-dir, calendar-mode
* [ ] `--calendar-mode` branch behavior test
* [ ] `--dry-run` ensures no file writes
* [ ] Keyboard interrupt: graceful shutdown
* [ ] Unicode support test across platforms
* [ ] Validate ICS RFC 5545 compliance (folding, encodings)
* [ ] Test import into Apple, Google, Outlook calendars

---

## 🧰 Developer Tooling

* [x] GitHub Actions CI (`ci.yml`)
* [x] Codecov badge + coverage reports
* [ ] Add `black` and `ruff` for style enforcement
* [ ] Add `mypy` static typing integration
* [ ] Configure `pre-commit` hooks
* [ ] Enable `dependabot.yml` for dependency updates

---

# 📊 Time Planning & Declarative Mode

Calmoji is evolving into more than a symbolic calendar generator — it's becoming a declarative planning tool that helps users align their intentions with how they actually spend time. This section outlines the next key steps toward that vision.

## 🛠️ Planner Infrastructure
* [ ] Add X-CALMOJI-* headers to all ICS events (e.g. X-CALMOJI-PROJECT, X-CALMOJI-SLOT, X-CALMOJI-SOURCE)
* [ ] Auto-generate PROJECT_ID from slugify(project name) if not specified
* [ ] Scaffold calmoji.yml config format (YAML-based weekly intent declaration)
* [ ] Implement calmoji plan --mode=declarative --next-week generator
* [ ] Create mapping logic between project labels and emoji slots
* [ ] Allow intuitive slot budgeting via percentage or slot count

## 📈 Weekly Summary Output
* [ ] Generate semantic summary (stdout and optional .txt)
 Example format:
```
Week W30 Summary:
  - Inari System: 6 slots (25.0%)
  - CVE RFCs:     4 slots (16.7%)
  - Family Time:  5 slots (20.8%)
  - Unassigned:   9 slots (37.5%) ❗️
```
* [ ] Highlight gaps, overages, and missing project IDs
* [ ] Optional output format: Markdown, plaintext, JSON

## 🔄 Feedback Loop
* [ ] In future: backfill used slots from exported calendar events
* [ ] Compare planned vs actual time
* [ ] Support symbolic drift analysis and coherence warnings

---

## ✨ Ready to contribute?

* Clone the repo
* `pip install -r dev-requirements.txt`
* Run `pytest -v --cov`
* Start with a small enhancement or test!
* Open a PR with a meaningful title + linked issue (if exists)

Let’s build something worthy of coherence. 🦊

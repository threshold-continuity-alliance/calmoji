This document defines our coverage targets and testing principles for the Calmoji codebase. Our goal is not merely 100% line coverage, but **meaningful, symbolic, and robust validation** of the timekeeping engine.

---

## 🎯 Coverage Targets by Layer

| Layer                    | Coverage Target          |
| ------------------------ | ------------------------ |
| `utils.py`               | 95–100%                  |
| `types.py`               | 100% (trivial)           |
| `ebi48.py`               | 100% (fixed map)         |
| `focus_blocks_writer.py` | 90%+                     |
| `slot_generator.py`      | 95%+                     |
| `cli.py` (TBD)           | 80%+                     |
| `ics_writer.py`          | 100% (esp. UID, folding) |

---

## 🛡️ Testing Principles

- All symbolic logic (e.g. EBI48, semantic slotting, weekly glyphs) must be **fully tested**
- Edge cases (DST, leap year, phase offset boundaries) must be covered
- Failing gracefully is as important as succeeding — test for bad inputs
- UID generation must be **deterministic, unique**, and reproducible
- ICS formatting must **respect RFC 5545** (e.g., line folding, encoding)
- Tests must work both in CI and local environments

---

## 🧰 Tooling

- [`pytest`](https://docs.pytest.org/)
- [`pytest-cov`](https://github.com/pytest-dev/pytest-cov)
- [`mypy`](http://mypy-lang.org/) for static typing
- [`ruff`](https://docs.astral.sh/ruff/) for formatting and linting
- [`black`](https://black.readthedocs.io/) for code consistency
- GitHub Actions CI for full test + coverage runs
- Codecov for badge and historical trend tracking

---

## 🧱 Thresholds

Calmoji CI will fail if:

- Global coverage drops below **90%**
- Any critical file drops more than **5% below its target**
- `--cov-branch` is not satisfied for core logic paths

---

We write tests not only for correctness,
but for **coherence**.

Let the fox mark what matters. 🦊
~
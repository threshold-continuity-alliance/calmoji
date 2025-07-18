# 🧿 calmoji

**The Ritual Calendar Crafter — Where Time Meets Glyph**
*...and where your visual cortex takes over from your guilt-ridden monkey mind!*

---

## 📖 What is calmoji?

**calmoji** is a handcrafted calendaring ritual tool that generates `.ics` files for your academic year — complete with phase-based planning blocks and visually anchored, emoji-clock-coded meeting slots.

This is not a generic scheduling app.
It is a **semantic time protocol**.
A **cognitive architecture**.
A tool to bring order, rhythm, and signal to your collaborative life.

You don’t schedule meetings with guilt.
You schedule them by asking:

> **“Which glyph aligns with your rhythm?”** 🐻🦊🦡🦉

---

## 🎯 Why This Exists

Most calendars are built for compliance — not cognition.

They assume your brain is a command-line buffer:
linear, overclocked, contextless.

But human minds aren’t machines. They are:

* **Visual**
* **Rhythmic**
* **Symbolic**
* **Context-sensitive**

**calmoji** is designed from first principles to support high-coherence scheduling across global teams, without sacrificing clarity or dignity.

It works by:

* Aligning to the **natural flow of the academic year**
* Building in **cognitive affordances** (25-min focus slots + decompression time)
* Anchoring to **global cities** and fair-time blocks
* Using **deterministic emoji-time tags** via [EBI48](https://ebi48.org)
* Outputting **modular, shareable `.ics` files** — ready to drop into any modern calendar

No apps. No cloud. Just clean, meaningful time encoded in human-readable glyphs.

Calmoji is not a scheduling app.

It's a **symbolic interface to time** — 
a **cognitive calendar protocol**.

---

## 🗺️ System Overview

### 📅 Academic Calendar Basis

Anchored on the European academic year (default: **September 15**).
Each year is divided into symbolic phases:

* Semester A (Seed)
* Winter Break
* Semester A (cont.)
* Downtime A→B
* Semester B (Flame)
* Summer Rest
* Deep Work Phase
* Preflight Prep
* Liminal Drift

Each phase outputs its own `.ics`.

### ⏰ Time Slot Design

Each participating weekday includes **8 meeting slots**, recurring every **3 weeks**, with:

* 25 minutes of focused conversation
* 5-minute decompression buffer
* Aligned to globally humane windows (e.g., 13:30–13:55 JST)

### 🌐 Time Zone Anchors

Slots are defined for:

* 🇳🇿 Auckland 🐨
* 🗼 Tokyo ⛩️
* 🕌 Delhi 🦚
* 🕋 Mecca 🐪
* 🏛 Brussels ⚛
* 🇨🇺 Havana 🌴
* ⛰️ Seattle 🌲

### 🧠 Emoji Time Protocol — `EBI48`

Each slot is tagged with a **unique emoji glyph**, deterministically mapped to one of 48 daily half-hour UTC segments.

This provides:

* Visual shorthand
* Cross-lingual clarity
* Low-bandwidth legibility
* Symbolic rhythm and recall

---

## 🔁 From Chaos to Canon

Originally, each slot used a randomized emoji — but this caused:

* Confusion across meetings
* Duplicate emojis per cycle
* No reliable naming convention

Now, [**EBI48**](https://ebi48.org) defines a canonical symbolic mapping:
**One emoji per half-hour slot, globally consistent.**

> “We could meet during **Fox Face**, **Worm Face**, or I’ve got 10 minutes at **Mountain Face 15** if that works?”

---

## 📦 Output

You’ll receive:

* `output/semester_phases_<year>.ics` — full-year phase blocks
* `output/meeting_<phase>_<dates>.ics` — detailed 25-min meeting slots

Each `VEVENT` includes:

```ics
SUMMARY: Tokyo 🐺 Wolf Face (13:30–13:55 JST)
DESCRIPTION: 🌱 — Semester A (Seed)
CLASS: PRIVATE
```

Also included:

* `output/ebi48_layer_<year>.ics` — a standalone emoji time overlay

---

## 🛠 Configuration

In `main.py` or CLI args:

* `--year=YYYY` → Academic year start
* `--dry-run` → Simulate without writing files
* Configurable slot cadence and region scope
* Deterministic UID generation for ICS re-import stability

**Pure Python 3 — no external dependencies required.**

---

## 🧪 Usage

```bash
git clone https://github.com/threshold-continuity-alliance/calmoji.git
cd calmoji/
python3 calmoji.py --year=2039
```

To preview the schedule structure without writing files:

```bash
python3 calmoji.py --year=2039 --dry-run
```

---

## 🙏 On Rhythmic Coexistence

**calmoji is secular — but rhythm-aware.**

We’ve cross-checked slot templates against Islamic prayer windows for empathy in scheduling:

| Prayer  | Local Time Range | Conflict Risk         |
| ------- | ---------------- | --------------------- |
| Fajr    | \~05:00–06:00    | ❌ None                |
| Dhuhr   | \~12:30–13:45    | ⚠️ Potential conflict |
| Asr     | \~15:30–17:30    | ✅ Avoided             |
| Maghrib | \~19:00–20:00    | ❌ None                |
| Isha    | \~20:00–22:00    | ❌ None                |

> Wherever you are: treat others' solar, cultural, and spiritual rhythms with **grace**.

---

## 💬 Suggested Usage Flow

1. Import the relevant `.ics` files into your calendar.

2. Ask collaborators:

   > “Which weekday and city block works for you?”

3. Choose a symbolic slot:

   > “Fox Face, Worm Face, or Mountain Face 15 are open on my end.”

4. Book the event, rename it with the participant's name.

---

## 🧭 Design Philosophy: Semantic Resilience

**calmoji** is a component of the [Threshold Continuity Alliance (TCA)](https://tca.earth/).

It is designed to:

* Withstand technological drift
* Remain interpretable across collapse
* Encode **meaning** in minimal forms

> If nothing survives but printed calendars and emoji glyphs,
> **Worm Face 13** will still make sense.

---

## 🙌 Credits

* 🧠 Ritual Design & Calendar Theory: **Trey Darley**
* 🔧 Semantic Architecture & Engineering: **ChatGPT**, **Claude**
* 🦊 Glyph Taste Consulting: **ChatGPT**
* 🌱 Stewardship: **Threshold Continuity Alliance (TCA)**

---

> Calendars should be kind.
> Time should be meaningful.
> **Coherence is not optional.**

**Fox Face out.** 🔥

---

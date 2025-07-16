# 🧿 Meetmoji Forge  
**The Ritual Calendar Crafter — Where Time Meets Glyph**  
*...and where your visual processing cortex takes over from your guilt-ridden monkey mind!*

---

## 📖 What is Meetmoji Forge?

**Meetmoji Forge** is a handcrafted calendaring ritual tool that generates .ics files for your academic year — complete with phase-based planning blocks and visually anchored, emoji-coded meeting slots.

It is not a generic scheduling app.  
It is a **semantic and cognitive system**, built from first principles to reduce scheduling fatigue, promote rhythm, and enable high-coherence collaboration across global time zones.

You don't schedule meetings with numbers or guilt.  
You schedule meetings by asking:  
**“What emoji are you today?”** 🐝🦊🌀🌿

---

## 🎯 Why This Exists

Traditional calendar systems are designed for corporate compliance — not creative clarity.  
Their UX treats your mind like a command-line buffer: linear, overloaded, guilt-prone.

But human cognition isn’t built like that.  
It’s *spatial*. *symbolic*. *visually driven*.

So we rebuilt scheduling:

- Using the **semesters of the academic year** as natural blocks for rhythm.
- Designing **time slots** that align with real-world cognitive stamina (24-minute blocks + decompression).
- Choosing **global-friendly time zones** mapped to major cities.
- Embedding **nature and animal emojis** to stimulate the visual cortex.
- Pre-generating 3-week rotation cycles so you never again ask: “When are you free?”

Meetmoji Forge encodes all this into shareable, modular `.ics` files.

You get structure, *without rigidity*.  
You get clarity, *without clutter*.  
And most of all, you **get to lead your schedule instead of being crushed by it**.

---

## 🗺️ System Overview

- 📅 **Academic Calendar Basis:**  
  Anchored on the **European university year** (September–September), with **two semesters**, clear **downtime**, and a **deep summer work phase**.

- ⏰ **Time Slots:**  
  Each weekday contains up to 10 × 24-minute slots (every 30 mins, with a 6-min decompression).  
  Events recur every **3 weeks** by default — allowing **natural pacing without burnout**.

- 🌍 **Timezone Anchoring:**  
  Slot blocks are designed to align with local lunch / afternoon hours in:
  - Tokyo
  - South Asia (Delhi)
  - Brussels
  - Washington DC
  - Seattle
  - *(Optionally: Oceania – Mondays and Fridays)*

- 🌀 **Emoji Assignment:**  
  Each slot is deterministically assigned a unique emoji — drawn from a carefully curated pool of 150 glyphs.  
  When scheduling a meeting, you just rename the emoji to the person's name, assign the Zoom link, and go.

- 📂 **Modular ICS Output:**  
  Each **phase** gets its own `.ics` file.  
  Each **meeting slot block** is structured with its emoji, time, and metadata in `SUMMARY` and `DESCRIPTION`.

---

## 🔧 How to Use

```bash
git clone https://github.com/admin-tca/meetmoji-forge.git
cd meetmoji-forge
python3 meetmoji_forge.py
```

## 🛠 Configuration
At the top of the script, you’ll find a clearly marked # 🔧 USER CONFIGURATION block.
There you can set:

  - Start date of the academic year (year_start)
  - Semester vs quarterly mode
  - Whether to include Oceania
  - Number of total cycles
  - Emoji reuse logic (per phase or global)

All configuration lives inside the Python file for now — no external dependencies.

## 📁 Output

The tool generates:

  - output/semester_phases.ics – all-day blocks for each phase (e.g., Semester A, Winter Break)
  - output/meeting_<phase_slug>.ics – detailed meeting slot files, one per phase
    
CLI --dry-run mode for inspection
CLI --year YYYY support for future academic years

Each event includes:

  - 📛 SUMMARY: E.g., Tokyo Slot 🐝 #12 (13:30–14:30 JST)
  - 🧾 DESCRIPTION: Auto-generated 🤖🔐☕️💬 — Semester A (Seed)
  - 🎨 (Optionally: ICS Category/Color tags)

## 📎 Suggested Workflow

1. Import the .ics files into your calendar.
2. When you want to book a 1:1:
  - Ask: “What city are you in, and what weekday works?”
  - Visually scan for that region’s emoji slots on that day.
  - Pick one. Rename the event’s emoji to their name. Done.
  - Tell them what emoji they are. It starts a conversation.
3. “Hey! You’re my 🐝 meeting this semester — perfect, you’re pollen-powered.”
  - It creates immediacy, identity, and a bond — without overhead.

## 🌀 Future Directions

  - 🧠 AI integration for predictive slot optimization
  - 📊 Visual printout calendar overlays
  - 📜 TCA-aligned “Time Rites” ceremonial framing (for TCA ritual integration)
  - 📆 Apple Shortcuts or mobile wrapper

# forge/meeting_slots.py

# 🕒 Meetmoji Anchor Slots — Always Local Time 13:30–14:30
# Times are expressed in UTC to align local anchors

# (Region, Start hour, Start minute, End hour, End minute, Local label)
MEETING_SLOTS = [
    ("Oceania",     5, 35, 6,  0,  "15:35–16:00 AEST"),  # Slot A
    ("Oceania",     6,  5, 6, 30,  "16:05–16:30 AEST"),  # Slot B
    ("Tokyo",       4, 35, 5,  0,  "13:35–14:00 JST"),   # Slot A
    ("Tokyo",       5,  5, 5, 30,  "14:05–14:30 JST"),   # Slot B
    ("South Asia",  7, 35, 8,  0,  "12:35–13:00 IST"),   # Slot A
    ("South Asia",  8,  5, 8, 30,  "13:05–13:30 IST"),   # Slot B
    ("Brussels",   11, 35, 12, 0,  "13:35–14:00 CEST"),  # Slot A
    ("Brussels",   12,  5, 12, 30, "14:05–14:30 CEST"),  # Slot B
    ("DC",         17, 35, 18, 0,  "13:35–14:00 EDT"),   # Slot A
    ("DC",         18,  5, 18, 30, "14:05–14:30 EDT"),   # Slot B
    ("Seattle",    20, 35, 21, 0,  "13:35–14:00 PDT"),   # Slot A
    ("Seattle",    21,  5, 21, 30, "14:05–14:30 PDT"),   # Slot B
]

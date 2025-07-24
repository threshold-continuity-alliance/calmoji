# calmoji/focus_blocks_config.py

# ⏳ Focus Block Config — UTC-based, 96m focus blocks with 24m gaps
# Each entry is: (Block Number, Start Hour, Start Minute, End Hour, End Minute, Emoji Label)

FOCUS_BLOCKS = [
    (1,  0,  0,  1, 36, "🧠"),     # Deep Thinking
    (2,  2,  0,  3, 36, "✍️"),     # Writing
    (3,  4,  0,  5, 36, "📚"),     # Reading
    (4,  6,  0,  7, 36, "🔧"),     # Technical
    (5,  8,  0,  9, 36, "🧾"),     # Admin
    (6, 10,  0, 11, 36, "📞"),     # Comms
    (7, 12,  0, 13, 36, "🪞"),     # Reflect
    (8, 14,  0, 15, 36, "📈"),     # Analysis
    (9, 16,  0, 17, 36, "🎨"),     # Creative
    (10, 18,  0, 19, 36, "🛠️"),    # Maintenance
    (11, 20,  0, 21, 36, "⚖️"),    # Decision
    (12, 22,  0, 23, 36, "⛩️"),    # Closure
]

# ACTIVE_WEEKDAYS: Optional override for days to include focus blocks (0 = Monday, 6 = Sunday)
# Set to None to use default full-week behavior
ACTIVE_WEEKDAYS = None  # Example override: [0, 1, 2, 3, 4] for Monday–Friday

# Default: all 7 days (Sunday to Saturday)
DEFAULT_ACTIVE_WEEKDAYS = list(range(7))  # [0, 1, 2, 3, 4, 5, 6]

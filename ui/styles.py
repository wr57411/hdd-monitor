"""
UI Styles and theme configuration for HDD Temperature Monitor
"""

from utils.config import COLORS, TEMP_NORMAL, TEMP_WARM

# Typography
FONT_FAMILY = "System"
FONT_TITLE = ("System", 18, "bold")
FONT_HEADER = ("System", 14, "bold")
FONT_BODY = ("System", 12)
FONT_LARGE = ("System", 48, "bold")
FONT_MEDIUM = ("System", 24, "bold")

# Card styling
CARD_PADX = 15
CARD_PADY = 15
CARD_IPADX = 10
CARD_IPADY = 10
CARD_BORDER_WIDTH = 0
CARD_RELIEF = "flat"

# Button styling
BUTTON_PADX = 12
BUTTON_PADY = 6
BUTTON_RELIEF = "flat"
BUTTON_BORDER_WIDTH = 0

# Layout
SECTION_SPACING = 10
WINDOW_PADDING = 20


def get_status_color(temp):
    """Get color based on temperature value"""
    if temp < TEMP_NORMAL:
        return COLORS["status_normal"]
    elif temp < TEMP_WARM:
        return COLORS["status_warm"]
    else:
        return COLORS["status_hot"]
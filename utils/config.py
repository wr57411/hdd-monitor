"""
Configuration and constants for HDD Temperature Monitor
"""

# Device Configuration
DEVICE_CONFIG = {
    "name": "ZHITAI TiPlus7100 1TB",
    "mount_point": "/Volumes/致态",
    "bsd_device": "disk6",  # Physical disk (disk7 is the volume/APFS slice)
    "smart_device": "/dev/disk6",
}

# Monitoring Intervals (in seconds)
UPDATE_INTERVAL = 3  # Main data update interval
POWER_UPDATE_INTERVAL = 10  # Power status update interval

# Temperature Thresholds (in Celsius)
TEMP_NORMAL = 45
TEMP_WARM = 60

# I/O Thresholds (for diagnostics)
IO_HIGH_THRESHOLD = 5000  # KB/s - high I/O activity
IO_MEDIUM_THRESHOLD = 1000  # KB/s - medium I/O activity

# Colors
COLORS = {
    "background": "#2D3748",  # Lighter background for visibility
    "card_bg": "#4A5568",     # Lighter card background
    "text_primary": "#FFFFFF",
    "text_secondary": "#E2E8F0",
    "status_normal": "#00C853",
    "status_warm": "#FF9800",
    "status_hot": "#F44336",
    "accent": "#00BCD4",
    "card_border": "#718096",
}
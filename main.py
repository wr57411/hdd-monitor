#!/usr/bin/python3
"""
HDD Temperature Monitor - Main Entry Point

A macOS GUI application for real-time monitoring of external HDD temperature,
I/O activity, and providing thermal diagnostics with actionable suggestions.

Run with: python3 main.py
Note: Requires system Python with Tkinter support (Python 3.9.6 on macOS)
"""

import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ui.dashboard import AppWindow
from utils.config import DEVICE_CONFIG, UPDATE_INTERVAL


def main():
    """Application entry point"""
    print("Starting application...")
    # Configure app
    config = {
        "mount_point": DEVICE_CONFIG["mount_point"],
        "bsd_device": DEVICE_CONFIG["bsd_device"],
        "smart_device": DEVICE_CONFIG["smart_device"],
        "update_interval": UPDATE_INTERVAL,
    }
    print("Config:", config)

    # Create and run application
    print("Creating AppWindow...")
    app = AppWindow(config)
    print("AppWindow created, calling run()...")
    app.run()
    print("AppWindow.run() returned")


if __name__ == "__main__":
    main()
#!/usr/bin/python3
"""
Debug test for HDD Monitor
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import tkinter as tk
from tkinter import ttk

print("Python version:", sys.version)
print("Tkinter version:", tk.TkVersion)

# Test 1: Create a simple window
print("\n=== Test 1: Simple window ===")
try:
    root = tk.Tk()
    root.title("Test Window")
    root.geometry("300x200+100+100")  # x, y position
    label = tk.Label(root, text="If you see this, tkinter works!")
    label.pack(expand=True)
    print("Window created, about to show...")
    root.update()  # Force window to appear
    print("Window should be visible now")
    root.after(2000, root.destroy)  # Close after 2 seconds
    root.mainloop()
    print("Test 1 completed")
except Exception as e:
    print("Test 1 failed:", e)
    import traceback
    traceback.print_exc()

# Test 2: Try to import and run our dashboard
print("\n=== Test 2: Import dashboard ===")
try:
    from ui.dashboard import AppWindow
    from utils.config import DEVICE_CONFIG, UPDATE_INTERVAL
    print("Imports successful")

    config = {
        "mount_point": DEVICE_CONFIG["mount_point"],
        "bsd_device": DEVICE_CONFIG["bsd_device"],
        "smart_device": DEVICE_CONFIG["smart_device"],
        "update_interval": UPDATE_INTERVAL,
    }
    print("Config:", config)

    # Create root window manually
    root = tk.Tk()
    root.title("HDD Monitor Debug")
    root.geometry("500x400+200+200")

    # Create dashboard inside this root
    dashboard = AppWindow(root, config)
    dashboard.pack(fill="both", expand=True)

    print("Dashboard created and packed")
    root.update()
    print("About to enter mainloop...")
    root.mainloop()
    print("Test 2 completed")
except Exception as e:
    print("Test 2 failed:", e)
    import traceback
    traceback.print_exc()
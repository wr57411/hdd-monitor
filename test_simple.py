#!/usr/bin/python3
"""
Simple tkinter test
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import tkinter as tk
from tkinter import ttk

def main():
    root = tk.Tk()
    root.title("Simple Test")
    root.geometry("400x300")

    label = tk.Label(root, text="If you see this, tkinter works!", font=("Arial", 16))
    label.pack(expand=True)

    button = ttk.Button(root, text="Quit", command=root.destroy)
    button.pack(pady=20)

    root.mainloop()

if __name__ == "__main__":
    main()
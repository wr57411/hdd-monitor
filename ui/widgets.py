"""
Custom widgets for HDD Temperature Monitor
"""

import tkinter as tk
from tkinter import ttk
from datetime import datetime

from .styles import FONT_HEADER, FONT_BODY, FONT_LARGE, FONT_MEDIUM, FONT_TITLE
from .styles import CARD_PADX, CARD_PADY, CARD_IPADX, CARD_IPADY, CARD_RELIEF, CARD_BORDER_WIDTH
from .styles import COLORS, SECTION_SPACING


class Card(tk.Frame):
    """Base card widget with consistent styling"""

    def __init__(self, parent, title=None, **kwargs):
        bg = kwargs.pop("bg", COLORS["card_bg"])
        super().__init__(parent, bg=bg, **kwargs)

        self.config(
            padx=CARD_PADX,
            pady=CARD_PADY,
            relief=CARD_RELIEF,
            borderwidth=CARD_BORDER_WIDTH
        )

        if title:
            title_label = tk.Label(
                self,
                text=title,
                font=FONT_HEADER,
                fg=COLORS["text_primary"],
                bg=bg,
                anchor="w"
            )
            title_label.pack(fill="x", pady=(0, 10))


class TemperatureCard(Card):
    """Temperature display card with status indicator"""

    def __init__(self, parent, **kwargs):
        super().__init__(parent, title="温度监控", **kwargs)

        # Temperature display
        self.temp_frame = tk.Frame(self, bg=self["bg"])
        self.temp_frame.pack(fill="x", pady=(0, 10))

        self.temp_value = tk.Label(
            self.temp_frame,
            text="--°C",
            font=FONT_LARGE,
            fg=COLORS["text_primary"],
            bg=self["bg"]
        )
        self.temp_value.pack(side="left")

        self.status_label = tk.Label(
            self.temp_frame,
            text="",
            font=FONT_BODY,
            fg=COLORS["text_secondary"],
            bg=self["bg"]
        )
        self.status_label.pack(side="right", padx=(10, 0))

        # Progress bar
        self.progress = ttk.Progressbar(
            self,
            length=200,
            maximum=100,
            mode="determinate"
        )
        self.progress.pack(fill="x")

        # Status text below progress bar
        self.status_text = tk.Label(
            self,
            text="正在获取温度...",
            font=FONT_BODY,
            fg=COLORS["text_secondary"],
            bg=self["bg"],
            anchor="w"
        )
        self.status_text.pack(fill="x", pady=(10, 0))

    def update(self, temp, status_text, status_color):
        """Update temperature display"""
        self.temp_value.config(text=f"{temp}°C", fg=status_color)
        self.status_label.config(text=status_text, fg=status_color)

        # Update progress bar (assuming max temp is 100°C)
        try:
            progress_value = min(int(temp), 100) if temp != "--" else 0
        except (ValueError, TypeError):
            progress_value = 0
        self.progress["value"] = progress_value

        # Configure progress bar color via style
        style = ttk.Style()
        style.configure(
            "Hottest.Horizontal.TProgressbar",
            troughcolor=COLORS["card_bg"],
            background=status_color
        )
        self.progress.configure(style="Hottest.Horizontal.TProgressbar")

        self.status_text.config(text=status_text, fg=status_color)


class IOCard(Card):
    """Disk I/O monitoring card"""

    def __init__(self, parent, **kwargs):
        super().__init__(parent, title="磁盘 I/O", **kwargs)

        # I/O stats grid
        info_frame = tk.Frame(self, bg=self["bg"])
        info_frame.pack(fill="x")

        # Read speed
        self.read_label = tk.Label(
            info_frame,
            text="读取: -- KB/s",
            font=FONT_BODY,
            fg=COLORS["text_primary"],
            bg=self["bg"],
            anchor="w"
        )
        self.read_label.pack(fill="x", pady=2)

        # Write speed
        self.write_label = tk.Label(
            info_frame,
            text="写入: -- KB/s",
            font=FONT_BODY,
            fg=COLORS["text_primary"],
            bg=self["bg"],
            anchor="w"
        )
        self.write_label.pack(fill="x", pady=2)

        # TPS
        self.tps_label = tk.Label(
            info_frame,
            text="TPS: --",
            font=FONT_BODY,
            fg=COLORS["text_secondary"],
            bg=self["bg"],
            anchor="w"
        )
        self.tps_label.pack(fill="x", pady=2)

    def update(self, read_kbs, write_kbs, tps):
        """Update I/O display"""
        self.read_label.config(text=f"读取: {read_kbs:.1f} KB/s" if read_kbs is not None else "读取: -- KB/s")
        self.write_label.config(text=f"写入: {write_kbs:.1f} KB/s" if write_kbs is not None else "写入: -- KB/s")
        self.tps_label.config(text=f"TPS: {tps:.1f}" if tps is not None else "TPS: --")


class ProcessCard(Card):
    """Active processes list card"""

    def __init__(self, parent, **kwargs):
        super().__init__(parent, title="活跃进程", **kwargs)

        # Process list using Listbox
        list_frame = tk.Frame(self, bg=self["bg"])
        list_frame.pack(fill="both", expand=True)

        self.process_list = tk.Listbox(
            list_frame,
            font=FONT_BODY,
            fg=COLORS["text_primary"],
            bg=self["bg"],
            selectbackground=COLORS["accent"],
            selectforeground=COLORS["text_primary"],
            borderwidth=0,
            highlightthickness=0,
            height=6
        )
        self.process_list.pack(fill="both", expand=True)

        # Scrollbar
        scrollbar = tk.Scrollbar(list_frame, orient="vertical", command=self.process_list.yview)
        self.process_list.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

    def update(self, processes):
        """Update process list"""
        self.process_list.delete(0, tk.END)

        if not processes:
            self.process_list.insert(0, "无活跃进程访问此磁盘")
        else:
            for proc in processes:
                display_text = f"{proc['pid']:>6}  {proc['command']:<15} {proc['type']}"
                self.process_list.insert(tk.END, display_text)

    def clear(self):
        """Clear process list"""
        self.process_list.delete(0, tk.END)
        self.process_list.insert(0, "正在获取进程信息...")


class DiagnosticsCard(Card):
    """Diagnostics and suggestions card"""

    def __init__(self, parent, **kwargs):
        super().__init__(parent, title="诊断与建议", **kwargs)

        # Cause label
        self.cause_frame = tk.Frame(self, bg=self["bg"])
        self.cause_frame.pack(fill="x", pady=(0, 10))

        cause_title = tk.Label(
            self.cause_frame,
            text="原因分析:",
            font=FONT_HEADER,
            fg=COLORS["text_secondary"],
            bg=self["bg"]
        )
        cause_title.pack(side="left")

        self.cause_label = tk.Label(
            self.cause_frame,
            text="--",
            font=FONT_BODY,
            fg=COLORS["text_primary"],
            bg=self["bg"]
        )
        self.cause_label.pack(side="left", padx=(5, 0))

        # Suggestion label
        suggestion_title = tk.Label(
            self,
            text="操作建议:",
            font=FONT_HEADER,
            fg=COLORS["text_secondary"],
            bg=self["bg"]
        )
        suggestion_title.pack(fill="x")

        self.suggestion_text = tk.Label(
            self,
            text="--",
            font=FONT_BODY,
            fg=COLORS["accent"],
            bg=self["bg"],
            anchor="w",
            wraplength=350,
            justify="left"
        )
        self.suggestion_text.pack(fill="x", pady=(5, 0))

    def update(self, cause, suggestion):
        """Update diagnostics display"""
        self.cause_label.config(text=cause)
        self.suggestion_text.config(text=suggestion)

    def clear(self):
        """Reset diagnostics"""
        self.cause_label.config(text="正在分析...")
        self.suggestion_text.config(text="--")


class Header(tk.Frame):
    """Application header with title and clock"""

    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)

        self.config(bg=COLORS["background"])

        # Title
        self.title_label = tk.Label(
            self,
            text="HDD Temperature Monitor",
            font=FONT_TITLE,
            fg=COLORS["text_primary"],
            bg=COLORS["background"]
        )
        self.title_label.pack(side="left")

        # Clock
        self.clock_label = tk.Label(
            self,
            text="",
            font=FONT_BODY,
            fg=COLORS["text_secondary"],
            bg=COLORS["background"]
        )
        self.clock_label.pack(side="right")

    def update_clock(self):
        """Update clock display"""
        now = datetime.now().strftime("%H:%M:%S")
        self.clock_label.config(text=now)
        self.after(1000, self.update_clock)


class Footer(tk.Frame):
    """Application footer with update status"""

    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)

        self.config(bg=COLORS["background"])

        self.status_label = tk.Label(
            self,
            text="正在初始化...",
            font=FONT_BODY,
            fg=COLORS["text_secondary"],
            bg=COLORS["background"]
        )
        self.status_label.pack(side="left")

    def update_status(self, message):
        """Update status message"""
        self.status_label.config(text=message)
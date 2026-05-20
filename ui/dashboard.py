"""
Main dashboard window for HDD Temperature Monitor
"""

import tkinter as tk
from datetime import datetime

from .widgets import (
    Header, Footer, TemperatureCard, IOCard, ProcessCard, DiagnosticsCard
)
from .styles import COLORS, SECTION_SPACING, WINDOW_PADDING
from monitors.temperature import TemperatureMonitor
from monitors.disk_io import IOMonitor
from monitors.processes import ProcessMonitor
from diagnostics.analyzer import DiagnosticsAnalyzer


class Dashboard(tk.Frame):
    """Main application dashboard"""

    def __init__(self, parent, config, **kwargs):
        super().__init__(parent, **kwargs)

        self.configure(bg=COLORS["background"])

        self.config = config
        self.update_count = 0

        # Initialize monitors
        self.temp_monitor = TemperatureMonitor(config)
        self.io_monitor = IOMonitor(config)
        self.process_monitor = ProcessMonitor(config)
        self.analyzer = DiagnosticsAnalyzer()

        # Build UI
        self._build_header()
        self._build_cards()
        self._build_footer()

        # Start monitoring
        self._start_monitoring()

    def _build_header(self):
        """Build header section"""
        self.header = Header(self, bg=COLORS["background"])
        self.header.pack(fill="x", pady=(0, SECTION_SPACING))
        self.header.update_clock()

    def _build_cards(self):
        """Build all monitoring cards"""
        cards_frame = tk.Frame(self, bg=COLORS["background"])
        cards_frame.pack(fill="both", expand=True)

        # Temperature card
        self.temp_card = TemperatureCard(cards_frame, bg=COLORS["card_bg"])
        self.temp_card.pack(fill="x", pady=(0, SECTION_SPACING))

        # I/O card
        self.io_card = IOCard(cards_frame, bg=COLORS["card_bg"])
        self.io_card.pack(fill="x", pady=(0, SECTION_SPACING))

        # Process card
        self.process_card = ProcessCard(cards_frame, bg=COLORS["card_bg"])
        self.process_card.pack(fill="both", expand=True, pady=(0, SECTION_SPACING))

        # Diagnostics card
        self.diagnostics_card = DiagnosticsCard(cards_frame, bg=COLORS["card_bg"])
        self.diagnostics_card.pack(fill="x", pady=(0, SECTION_SPACING))

    def _build_footer(self):
        """Build footer section"""
        self.footer = Footer(self, bg=COLORS["background"])
        self.footer.pack(fill="x", pady=(SECTION_SPACING, 0))

    def _start_monitoring(self):
        """Start the monitoring loop"""
        self._update()

    def _update(self):
        """Update all monitoring data"""
        self.update_count += 1

        try:
            # Get temperature
            temp_data = self.temp_monitor.get_temperature()
            temp = temp_data.get("temperature")
            temp_raw = temp_data.get("raw", "N/A")

            # Get I/O stats
            io_data = self.io_monitor.get_stats()
            read_kbs = io_data.get("read_kbs")
            write_kbs = io_data.get("write_kbs")
            tps = io_data.get("tps")

            # Get processes
            processes = self.process_monitor.get_processes()

            # Update temperature card
            if temp is not None:
                # Determine status
                if temp < 45:
                    status_text = "正常"
                    status_color = COLORS["status_normal"]
                elif temp < 60:
                    status_text = "轻微发热"
                    status_color = COLORS["status_warm"]
                else:
                    status_text = "明显发热"
                    status_color = COLORS["status_hot"]

                self.temp_card.update(temp, status_text, status_color)
            else:
                self.temp_card.update("--", "无法获取", COLORS["text_secondary"])

            # Update I/O card
            self.io_card.update(read_kbs, write_kbs, tps)

            # Update process card
            self.process_card.update(processes)

            # Analyze and update diagnostics
            diagnostics = self.analyzer.analyze(
                temperature=temp,
                read_kbs=read_kbs,
                write_kbs=write_kbs,
                tps=tps,
                processes=processes
            )

            self.diagnostics_card.update(
                diagnostics.get("cause", "正在分析..."),
                diagnostics.get("suggestion", "--")
            )

            # Update footer
            self.footer.update_status(f"最后更新: {datetime.now().strftime('%H:%M:%S')}")

        except Exception as e:
            self.footer.update_status(f"错误: {str(e)}")

        # Schedule next update
        interval = self.config.get("update_interval", 3) * 1000
        self.after(interval, self._update)

    def on_close(self):
        """Cleanup on window close"""
        pass  # Monitors don't require cleanup in this implementation


class AppWindow:
    """Main application window"""

    def __init__(self, config):
        self.config = config

        # Create root window
        self.root = tk.Tk()
        self.root.title("HDD Temperature Monitor")
        self.root.configure(bg=COLORS["background"])

        # Set window size and position
        width = 480
        height = 720
        x = (self.root.winfo_screenwidth() - width) // 2
        y = (self.root.winfo_screenheight() - height) // 2
        self.root.geometry(f"{width}x{height}+{x}+{y}")

        # Make window non-resizable
        self.root.resizable(False, False)

        # Create dashboard
        self.dashboard = Dashboard(self.root, config, bg=COLORS["background"])
        self.dashboard.pack(fill="both", expand=True, padx=WINDOW_PADDING, pady=WINDOW_PADDING)

        # Handle window close
        self.root.protocol("WM_DELETE_WINDOW", self._on_close)
        self.root.bind("<Command-q>", lambda e: self._on_close())

    def run(self):
        """Start the application"""
        self.root.mainloop()

    def _on_close(self):
        """Handle window close event"""
        self.dashboard.on_close()
        self.root.destroy()
"""
Disk I/O monitor using iostat (macOS version)
"""

import subprocess
import re


class IOMonitor:
    """Monitor disk I/O statistics"""

    def __init__(self, config):
        self.mount_point = config.get("mount_point", "/Volumes/致态")
        self.bsd_device = config.get("bsd_device", "disk7")

    def get_stats(self):
        """
        Get disk I/O statistics

        Returns:
            dict with 'read_kbs', 'write_kbs', 'tps' (all float or None)
        """
        result = {
            "read_kbs": None,
            "write_kbs": None,
            "tps": None
        }

        try:
            # macOS iostat: -d: disk utilization, interval 2, count 1
            cmd = ["iostat", "-d", "2", "1", self.bsd_device]
            output = subprocess.check_output(
                cmd,
                stderr=subprocess.DEVNULL,
                timeout=10
            ).decode("utf-8", errors="ignore")

            result = self._parse_iostat(output)

        except (subprocess.TimeoutExpired, subprocess.CalledProcessError, FileNotFoundError):
            # Try alternative: just interval 2 without count
            try:
                cmd = ["iostat", "-d", "2", self.bsd_device]
                output = subprocess.check_output(
                    cmd,
                    stderr=subprocess.DEVNULL,
                    timeout=10
                ).decode("utf-8", errors="ignore")
                result = self._parse_iostat(output)
            except Exception:
                pass

        return result

    def _parse_iostat(self, output):
        """
        Parse iostat output to extract disk6 stats

        macOS iostat -d format (multi-device per line):
        device         KB/t  tps  MB/s     KB/t  tps  MB/s
        disk0         23.49  276  6.33    17.42    8  0.13

        All devices' stats are on a single line, separated by whitespace.
        We need to find which column range belongs to our target device.
        """
        result = {
            "read_kbs": None,
            "write_kbs": None,
            "tps": None
        }

        lines = output.split("\n")
        if len(lines) < 3:
            return result

        header_line = lines[0]
        data_line = lines[2]  # Data is on line index 2 (0=devices, 1=header, 2=data)

        # Find column positions for each device in header
        header_devices = header_line.split()
        data_values = data_line.split()

        # Find index of our target device in header
        try:
            device_idx = header_devices.index(self.bsd_device)
        except ValueError:
            return result

        # Each device has 3 values (KB/t, tps, MB/s)
        # Values are interleaved: disk0_KBt disk0_tps disk0_MBs disk1_KBt disk1_tps disk1_MBs ...
        base_idx = device_idx * 3  # Position of KB/t for our device

        try:
            kb_per_transfer = float(data_values[base_idx])
            tps = float(data_values[base_idx + 1])
            mb_per_s = float(data_values[base_idx + 2])

            result["tps"] = tps
            # KB/s = KB/t * tps
            result["read_kbs"] = kb_per_transfer * tps
            result["write_kbs"] = 0.0  # Cannot distinguish on macOS
        except (IndexError, ValueError):
            pass

        return result
"""
Process monitor using lsof
"""

import subprocess
import re


class ProcessMonitor:
    """Monitor processes accessing the disk"""

    def __init__(self, config):
        self.mount_point = config.get("mount_point", "/Volumes/致态")

    def get_processes(self):
        """
        Get list of processes accessing the mount point

        Returns:
            list of dicts with 'pid', 'command', 'type', 'bytes'
        """
        processes = []

        try:
            # Run lsof to find processes accessing the mount point
            # +D: find all processes accessing directory and subdirectories
            cmd = ["lsof", "+D", self.mount_point]
            output = subprocess.check_output(
                cmd,
                stderr=subprocess.DEVNULL,
                timeout=15
            ).decode("utf-8", errors="ignore")

            processes = self._parse_lsof(output)

        except (subprocess.TimeoutExpired, subprocess.CalledProcessError, FileNotFoundError):
            pass

        return processes

    def _parse_lsof(self, output):
        """
        Parse lsof output to extract process information

        lsof output format:
        COMMAND     PID   USER   FD   TYPE   DEVICE   SIZE/OFF   NODE   NAME
        Finder      1234  user    4r  DIR    disk7s1  4096       1234   /Volumes/致态
        """
        processes = []
        lines = output.split("\n")

        seen_pids = set()

        for line in lines[1:]:  # Skip header line
            if not line.strip():
                continue

            parts = line.split()
            if len(parts) < 2:
                continue

            try:
                command = parts[0]
                pid = parts[1]

                # Skip duplicates
                if pid in seen_pids:
                    continue
                seen_pids.add(pid)

                # Determine access type based on FD column
                access_type = "unknown"
                if len(parts) >= 4:
                    fd = parts[3]
                    if "r" in fd.lower():
                        access_type = "read"
                    elif "w" in fd.lower():
                        access_type = "write"
                    elif "u" in fd.lower():
                        access_type = "read/write"

                processes.append({
                    "pid": pid,
                    "command": command,
                    "type": access_type,
                    "bytes": None
                })

            except (IndexError, ValueError):
                continue

        return processes
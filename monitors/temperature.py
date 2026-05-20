"""
Temperature monitor using SMART data
"""

import subprocess
import re


class TemperatureMonitor:
    """Monitor disk temperature via SMART"""

    def __init__(self, config):
        self.mount_point = config.get("mount_point", "/Volumes/致态")
        self.bsd_device = config.get("bsd_device", "disk7")
        self.smart_device = config.get("smart_device", "/dev/disk7")

    def get_temperature(self):
        """
        Get disk temperature from SMART data

        Returns:
            dict with 'temperature' (int or None) and 'raw' (str)
        """
        result = {
            "temperature": None,
            "raw": "N/A",
            "available": False
        }

        # Try smartctl first
        temp = self._get_smart_temp()
        if temp is not None:
            result["temperature"] = temp
            result["raw"] = f"SMART: {temp}°C"
            result["available"] = True
            return result

        # Try system_profiler as fallback
        temp = self._get_system_profiler_temp()
        if temp is not None:
            result["temperature"] = temp
            result["raw"] = f"system_profiler: {temp}°C"
            result["available"] = True
            return result

        return result

    def _get_smart_temp(self):
        """Get temperature from smartctl command"""
        try:
            cmd = ["smartctl", "-a", self.smart_device]
            output = subprocess.check_output(cmd, stderr=subprocess.DEVNULL, timeout=10).decode("utf-8", errors="ignore")

            # Look for temperature lines in NVMe SMART output
            # NVMe format: "Temperature:                        X Celsius"
            for line in output.split("\n"):
                line_lower = line.lower()
                if "temperature" in line_lower and "celsius" in line_lower:
                    # Extract temperature value
                    match = re.search(r"(\d+)\s+Celsius", line, re.IGNORECASE)
                    if match:
                        return int(match.group(1))

                # Alternative format for some drives
                if "temp" in line_lower and "raw" not in line_lower:
                    match = re.search(r"temperature\s+:\s+(\d+)", line, re.IGNORECASE)
                    if match:
                        return int(match.group(1))

        except (subprocess.TimeoutExpired, subprocess.CalledProcessError, FileNotFoundError):
            pass

        return None

    def _get_system_profiler_temp(self):
        """Get temperature from system_profiler"""
        try:
            cmd = ["system_profiler", "SPNVMeDataType"]
            output = subprocess.check_output(cmd, stderr=subprocess.DEVNULL, timeout=10).decode("utf-8", errors="ignore")

            # Look for temperature in NVMe data
            for line in output.split("\n"):
                if "temperature" in line.lower() or "temp" in line.lower():
                    match = re.search(r"(\d+)\s*°?C", line, re.IGNORECASE)
                    if match:
                        return int(match.group(1))

        except (subprocess.TimeoutExpired, subprocess.CalledProcessError, FileNotFoundError):
            pass

        return None
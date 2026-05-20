"""
Diagnostics analyzer for HDD thermal issues
"""

from utils.config import TEMP_NORMAL, TEMP_WARM, IO_HIGH_THRESHOLD, IO_MEDIUM_THRESHOLD


class DiagnosticsAnalyzer:
    """Analyze temperature and I/O data to diagnose thermal issues"""

    def __init__(self):
        pass

    def analyze(self, temperature, read_kbs, write_kbs, tps, processes):
        """
        Analyze collected data and provide diagnostics

        Args:
            temperature: int or None (Celsius)
            read_kbs: float or None (KB/s)
            write_kbs: float or None (KB/s)
            tps: float or None (transactions per second)
            processes: list of process dicts

        Returns:
            dict with 'cause' and 'suggestion'
        """
        result = {
            "cause": "正在分析...",
            "suggestion": "等待数据..."
        }

        # Calculate total I/O
        total_io = 0
        if read_kbs is not None:
            total_io += read_kbs
        if write_kbs is not None:
            total_io += write_kbs

        # Count active processes
        num_processes = len(processes) if processes else 0

        # Determine state based on temperature
        if temperature is None:
            # Cannot determine temperature
            result["cause"] = "无法获取温度数据"
            result["suggestion"] = "请检查硬盘是否正确连接"
            return result

        if temperature >= TEMP_WARM:
            # Hot state
            return self._analyze_hot(total_io, num_processes, processes)
        elif temperature >= TEMP_NORMAL:
            # Warm state
            return self._analyze_warm(total_io, num_processes, processes)
        else:
            # Normal state
            return self._analyze_normal(total_io, num_processes, processes)

    def _analyze_hot(self, total_io, num_processes, processes):
        """Analyze when temperature is hot (>60°C)"""
        if num_processes > 2:
            return {
                "cause": "多程序同时访问磁盘导致发热",
                "suggestion": "关闭不需要的应用程序，减少并发访问"
            }
        elif total_io > IO_HIGH_THRESHOLD:
            return {
                "cause": "持续大量读写导致发热",
                "suggestion": "暂停大型文件传输或备份任务"
            }
        elif total_io > IO_MEDIUM_THRESHOLD:
            return {
                "cause": "中等 I/O 负载导致发热",
                "suggestion": "减少磁盘访问，给硬盘散热时间"
            }
        else:
            return {
                "cause": "散热不良导致发热",
                "suggestion": "检查硬盘通风条件，关闭笔记本盖子可能影响散热"
            }

    def _analyze_warm(self, total_io, num_processes, processes):
        """Analyze when temperature is warm (45-60°C)"""
        if num_processes > 3:
            return {
                "cause": "多程序争用磁盘资源",
                "suggestion": "关闭不需要的进程，减少争用"
            }
        elif total_io > IO_HIGH_THRESHOLD:
            return {
                "cause": "较高 I/O 活动导致轻微发热",
                "suggestion": "监控磁盘活动，避免持续高负载"
            }
        elif total_io > IO_MEDIUM_THRESHOLD:
            return {
                "cause": "适度 I/O 导致轻微发热",
                "suggestion": "状态正常，但注意持续负载"
            }
        else:
            return {
                "cause": "硬盘自然发热（无高负载）",
                "suggestion": "当前状态正常，保持监控即可"
            }

    def _analyze_normal(self, total_io, num_processes, processes):
        """Analyze when temperature is normal (<45°C)"""
        if num_processes > 3:
            return {
                "cause": "多程序访问但温度正常",
                "suggestion": "磁盘散热良好，无需操作"
            }
        elif total_io > IO_HIGH_THRESHOLD:
            return {
                "cause": "高 I/O 活动（温度正常）",
                "suggestion": "当前状态良好，注意长时间高负载"
            }
        elif total_io > IO_MEDIUM_THRESHOLD:
            return {
                "cause": "正常 I/O 活动",
                "suggestion": "磁盘使用正常，无发热问题"
            }
        else:
            return {
                "cause": "磁盘空闲或低负载",
                "suggestion": "当前状态良好，硬盘温度正常"
            }
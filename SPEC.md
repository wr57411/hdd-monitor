# HDD Temperature Monitor - Specification

## 1. Project Overview

**Project Name**: HDD Temperature Monitor
**Type**: macOS GUI Application
**Core Functionality**: Real-time monitoring of external HDD temperature, I/O activity, and providing thermal diagnostics with actionable suggestions.
**Target Users**: Users with external storage devices who need to monitor thermal health.

---

## 2. Target Device

| Attribute | Value |
|-----------|-------|
| Model | ZHITAI TiPlus7100 1TB |
| Interface | ASMedia 246x (USB4/Thunderbolt) |
| Mount Point | /Volumes/致态 |
| BSD Device | disk7 |

---

## 3. UI/UX Specification

### 3.1 Window Configuration
- **Window Size**: 480 x 720 pixels
- **Window Title**: HDD Temperature Monitor
- **Window Style**: Native macOS appearance with dark theme
- **Position**: Centered on screen

### 3.2 Color Palette
| Usage | Color | Hex Code |
|-------|-------|----------|
| Background | Dark Gray | #1E1E1E |
| Card Background | Slightly Lighter | #2D2D2D |
| Primary Text | White | #FFFFFF |
| Secondary Text | Light Gray | #B0B0B0 |
| Normal Status | Green | #00C853 |
| Warm Status | Orange | #FF9800 |
| Hot Status | Red | #F44336 |
| Accent | Cyan | #00BCD4 |

### 3.3 Typography
- **Font Family**: System font (San Francisco on macOS)
- **Title Size**: 18px bold
- **Card Header**: 14px bold
- **Body Text**: 12px regular
- **Large Display (Temperature)**: 48px bold
- **Medium Display**: 24px bold

### 3.4 Layout Structure

```
+------------------------------------------+
|  HDD Temperature Monitor      12:34:56   |  <- Header
+------------------------------------------+
|                                          |
|  +------------------------------------+  |
|  |     TEMPERATURE CARD               |  |
|  |     [=========-----] 52°C           |  |  <- Temperature Display
|  |     Status: Slightly Warm          |  |
|  +------------------------------------+  |
|                                          |
|  +------------------------------------+  |
|  |     I/O MONITOR                    |  |
|  |     Read:  125 KB/s                |  |
|  |     Write: 89 KB/s                 |  |  <- I/O Stats
|  |     TPS:   24                     |  |
|  +------------------------------------+  |
|                                          |
|  +------------------------------------+  |
|  |     ACTIVE PROCESSES               |  |
|  |     PID   CMD        TYPE          |  |
|  |     1234  Finder     read          |  |  <- Process List
|  |     5678  backup    write         |  |
|  +------------------------------------+  |
|                                          |
|  +------------------------------------+  |
|  |     DIAGNOSTICS                    |  |
|  |     Cause: Moderate I/O activity  |  |
|  |     Suggestion:                   |  |
|  |     [Close unnecessary apps]       |  |  <- Action Items
|  +------------------------------------+  |
|                                          |
|  Last updated: 3 seconds ago             |  <- Footer
+------------------------------------------+
```

---

## 4. Functional Specification

### 4.1 Data Collection

| Data | Source Command | Update Interval |
|------|---------------|-----------------|
| Temperature | `smartctl -a /dev/disk7 2>/dev/null \| grep -i temp` | 3 seconds |
| Disk I/O | `iostat -x 5 2>/dev/null` (parse disk7) | 3 seconds |
| Active Processes | `lsof +D /Volumes/致态 2>/dev/null` | 3 seconds |
| Power Status | `pmset -g 2>/dev/null` | 10 seconds |

### 4.2 Temperature Thresholds

| State | Temperature Range | Visual Indicator |
|-------|-------------------|------------------|
| Normal | < 45°C | Green (#00C853) |
| Warm | 45°C - 60°C | Orange (#FF9800) |
| Hot | > 60°C | Red (#F44336) |

### 4.3 Diagnostics Logic

**Diagnostic Rules**:
1. **High I/O + High Temperature** → "持续大量读写导致发热"
2. **Multiple Active Processes + High Temperature** → "多程序争用磁盘"
3. **High Temperature + No Active Processes** → "散热不良，建议检查通风"
4. **Normal Temperature + Active I/O** → "磁盘正在被正常使用"
5. **Normal Temperature + No I/O** → "当前状态良好"

### 4.4 Action Suggestions

| Diagnostic | Action |
|------------|--------|
| 持续大量读写 | "暂停大型文件传输任务" |
| 多程序争用 | "关闭不需要的程序" |
| 散热不良 | "改善硬盘通风，关闭笔记本盖子" |
| 正常使用 | "无需操作" |
| 状态良好 | "当前状态良好，继续保持" |

---

## 5. Technical Architecture

### 5.1 Project Structure

```
hdd-monitor/
├── SPEC.md
├── requirements.txt
├── main.py
├── ui/
│   ├── __init__.py
│   ├── dashboard.py
│   ├── widgets.py
│   └── styles.py
├── monitors/
│   ├── __init__.py
│   ├── temperature.py
│   ├── disk_io.py
│   └── processes.py
├── diagnostics/
│   ├── __init__.py
│   └── analyzer.py
└── utils/
    ├── __init__.py
    └── config.py
```

### 5.2 Module Responsibilities

**main.py**: Application entry point, initializes Tkinter window
**ui/dashboard.py**: Main dashboard container and layout
**ui/widgets.py**: Reusable card widgets (TemperatureCard, IOCard, ProcessCard, DiagnosticsCard)
**ui/styles.py**: Color and typography definitions
**monitors/temperature.py**: SMART temperature data collector
**monitors/disk_io.py**: I/O statistics collector using iostat
**monitors/processes.py**: Process monitoring using lsof
**diagnostics/analyzer.py**: Thermal diagnosis engine
**utils/config.py**: Device configuration and constants

---

## 6. Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| Python | 3.10+ | Runtime (built-in) |
| Tkinter | built-in | GUI framework |

**No external dependencies required** - all functionality uses macOS built-in commands.

---

## 7. Acceptance Criteria

1. Application launches without errors on macOS
2. Temperature display updates every 3 seconds
3. I/O statistics display correctly (Read KB/s, Write KB/s, TPS)
4. Process list shows currently active processes accessing the mount point
5. Color indicators change based on temperature thresholds
6. Diagnostics card updates based on combined data analysis
7. All text is clearly readable on dark background
8. Window is properly centered and sized at 480x720
9. Application can be terminated gracefully with Cmd+Q
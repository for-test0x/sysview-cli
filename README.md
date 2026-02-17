# ⚡ SysView CLI

**A beautiful, colorful terminal system monitor for Linux**

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Platform](https://img.shields.io/badge/platform-Linux%20%7C%20macOS-lightgrey.svg)

SysView CLI transforms your terminal into a stunning system dashboard with colorful graphics, progress bars, and intuitive data visualization. Monitor CPU, RAM, disk, network, battery, and temperatures — all from your terminal.

```
  ____            __     ___               
 / ___| _   _ ___\ \   / (_) _____      __
 \___ \| | | / __| \ \ / /| |/ _ \ \ /\ / /
  ___) | |_| \__ \  \ V / | |  __/\ V  V / 
 |____/ \__, |___/   \_/  |_|\___| \_/\_/  
        |___/                    CLI v1.0.0
```

## 🎨 Features

- **📋 System Info** — Hostname, OS, architecture, processor, uptime
- **🔥 CPU Monitor** — Total + per-core usage with color-coded progress bars
- **🧠 Memory** — RAM and Swap usage with visual indicators
- **💾 Disk Partitions** — All mounted drives with usage bars
- **🌐 Network** — Traffic stats and interface details
- **🔋 Battery & Sensors** — Battery status and temperature readings
- **📊 Export** — JSON and HTML report generation
- **🔄 Live Mode** — Auto-refreshing dashboard

## 🚀 Installation

### Quick Install (recommended)

```bash
curl -sSL https://raw.githubusercontent.com/for-test0x/sysview-cli/main/install.sh | bash
```

### Manual Install

```bash
# 1. Clone the repo
git clone https://github.com/for-test0x/sysview-cli.git
cd sysview-cli

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run
python3 -m sysview
```

### Install as command (optional)

After cloning, you can create a global command:

```bash
# Create launcher
mkdir -p ~/.local/bin
echo '#!/bin/bash
cd ~/sysview-cli && python3 -m sysview "$@"' > ~/.local/bin/sysview
chmod +x ~/.local/bin/sysview

# Add to PATH (if not already)
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
```

Now just run `sysview` from anywhere.

## 📖 Usage

```bash
# Single snapshot dashboard
sysview

# Live monitoring (auto-refresh every 2 seconds)
sysview --live

# Custom refresh interval
sysview --live -i 5

# Export as JSON
sysview --json

# Export as HTML report
sysview --html report.html

# Show help
sysview --help
```

## 📸 Preview

The dashboard displays color-coded panels in your terminal:

```
╭──────── 📋 System Information ────────╮
│  🖥  Hostname    my-server             │
│  🐧 OS          Ubuntu 22.04          │
│  🏗  Arch        x86_64                │
│  ⏱  Uptime      3d 14h 22m            │
╰───────────────────────────────────────╯
╭──────── 🔥 CPU Usage ────────────────╮
│  TOTAL ████████████░░░░░░░░ 58.3%     │
│  Core 0 ██████████████░░░░ 72.1%      │
│  Core 1 ██████░░░░░░░░░░░░ 31.5%      │
╰───────────────────────────────────────╯
╭──────── 🧠 Memory ──────────────────╮
│  RAM  █████████████░░░░░░░ 64.2%      │
│  Total: 16.0 GB | Used: 10.3 GB      │
╰───────────────────────────────────────╯
```

Colors change based on usage: 🟢 low → 🟡 medium → 🟠 high → 🔴 critical

## 🔧 Requirements

- Python 3.8+
- Linux or macOS
- Terminal with Unicode support

## 📝 License

MIT License - See [LICENSE](LICENSE) for details.

## 🤝 Contributing

Contributions welcome! Open an issue or submit a pull request.

---

**Made with ❤ by**

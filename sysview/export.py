"""
Export system information to different formats
"""

import json
import datetime
from typing import Dict, Any

from .system_info import (
    get_system_info,
    get_cpu_info,
    get_memory_info,
    get_disk_info,
    get_network_info,
    get_process_info,
    get_battery_info,
    format_bytes,
)
from . import __version__


def export_json() -> Dict[str, Any]:
    """Export all system info as a dictionary."""
    mem = get_memory_info()
    return {
        "timestamp": datetime.datetime.now().isoformat(),
        "sysview_version": __version__,
        "system": get_system_info(),
        "cpu": get_cpu_info(),
        "memory": {
            "ram": {
                "total": format_bytes(mem["total"]),
                "used": format_bytes(mem["used"]),
                "available": format_bytes(mem["available"]),
                "percent": mem["percent"],
            },
            "swap": {
                "total": format_bytes(mem["swap_total"]),
                "used": format_bytes(mem["swap_used"]),
                "percent": mem["swap_percent"],
            },
        },
        "disks": [
            {
                "device": d["device"],
                "mountpoint": d["mountpoint"],
                "fstype": d["fstype"],
                "total": format_bytes(d["total"]),
                "used": format_bytes(d["used"]),
                "free": format_bytes(d["free"]),
                "percent": d["percent"],
            }
            for d in get_disk_info()
        ],
        "network": get_network_info(),
        "processes": get_process_info(top_n=10),
        "battery": get_battery_info(),
    }


def export_html(output_path: str):
    """Export system information as a styled HTML report."""
    data = export_json()
    sys_info = data["system"]
    cpu_info = data["cpu"]
    mem_info = data["memory"]

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SysView Report - {sys_info['hostname']}</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: 'Segoe UI', system-ui, -apple-system, sans-serif;
            background: #0a0a1a;
            color: #e0e0e0;
            padding: 20px;
        }}
        .container {{ max-width: 1200px; margin: 0 auto; }}
        h1 {{
            text-align: center;
            font-size: 2.5em;
            background: linear-gradient(135deg, #00d4ff, #7b2fff, #ff2d95);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 5px;
        }}
        .subtitle {{
            text-align: center;
            color: #888;
            margin-bottom: 30px;
        }}
        .grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-bottom: 20px; }}
        .card {{
            background: #12122a;
            border: 1px solid #2a2a4a;
            border-radius: 12px;
            padding: 20px;
            transition: border-color 0.3s;
        }}
        .card:hover {{ border-color: #00d4ff; }}
        .card h2 {{
            font-size: 1.2em;
            color: #00d4ff;
            margin-bottom: 15px;
            padding-bottom: 8px;
            border-bottom: 1px solid #2a2a4a;
        }}
        .card.full {{ grid-column: 1 / -1; }}
        .stat-row {{
            display: flex;
            justify-content: space-between;
            padding: 6px 0;
            border-bottom: 1px solid #1a1a3a;
        }}
        .stat-label {{ color: #888; }}
        .stat-value {{ color: #fff; font-weight: 600; }}
        .progress-bar {{
            height: 10px;
            background: #1a1a3a;
            border-radius: 5px;
            overflow: hidden;
            margin: 8px 0;
        }}
        .progress-fill {{
            height: 100%;
            border-radius: 5px;
            transition: width 0.5s;
        }}
        .green {{ background: linear-gradient(90deg, #00c853, #64dd17); }}
        .yellow {{ background: linear-gradient(90deg, #ffd600, #ffab00); }}
        .orange {{ background: linear-gradient(90deg, #ff9100, #ff6d00); }}
        .red {{ background: linear-gradient(90deg, #ff5252, #d50000); }}
        table {{
            width: 100%;
            border-collapse: collapse;
        }}
        th, td {{
            padding: 8px 12px;
            text-align: left;
            border-bottom: 1px solid #1a1a3a;
        }}
        th {{ color: #00d4ff; font-weight: 600; }}
        .footer {{
            text-align: center;
            padding: 20px;
            color: #555;
            margin-top: 30px;
            border-top: 1px solid #2a2a4a;
        }}
        .footer a {{ color: #7b2fff; text-decoration: none; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>⚡ SysView Report</h1>
        <p class="subtitle">Generated on {data['timestamp'][:19]} | SysView CLI v{__version__}</p>

        <div class="grid">
            <div class="card">
                <h2>📋 System Information</h2>
                <div class="stat-row"><span class="stat-label">Hostname</span><span class="stat-value">{sys_info['hostname']}</span></div>
                <div class="stat-row"><span class="stat-label">OS</span><span class="stat-value">{sys_info['os']}</span></div>
                <div class="stat-row"><span class="stat-label">Architecture</span><span class="stat-value">{sys_info['architecture']}</span></div>
                <div class="stat-row"><span class="stat-label">Processor</span><span class="stat-value">{sys_info['processor'][:40]}</span></div>
                <div class="stat-row"><span class="stat-label">Uptime</span><span class="stat-value">{sys_info['uptime']}</span></div>
            </div>

            <div class="card">
                <h2>🔥 CPU</h2>
                <div class="stat-row"><span class="stat-label">Physical Cores</span><span class="stat-value">{cpu_info['physical_cores']}</span></div>
                <div class="stat-row"><span class="stat-label">Logical Cores</span><span class="stat-value">{cpu_info['logical_cores']}</span></div>
                <div class="stat-row"><span class="stat-label">Frequency</span><span class="stat-value">{cpu_info['current_frequency']}</span></div>
                <div class="stat-row"><span class="stat-label">Total Usage</span><span class="stat-value">{cpu_info['total_usage']}%</span></div>
                <div class="progress-bar">
                    <div class="progress-fill {'green' if cpu_info['total_usage'] < 30 else 'yellow' if cpu_info['total_usage'] < 60 else 'orange' if cpu_info['total_usage'] < 80 else 'red'}" style="width: {cpu_info['total_usage']}%"></div>
                </div>
            </div>

            <div class="card">
                <h2>🧠 Memory</h2>
                <div class="stat-row"><span class="stat-label">RAM Total</span><span class="stat-value">{mem_info['ram']['total']}</span></div>
                <div class="stat-row"><span class="stat-label">RAM Used</span><span class="stat-value">{mem_info['ram']['used']}</span></div>
                <div class="stat-row"><span class="stat-label">RAM Available</span><span class="stat-value">{mem_info['ram']['available']}</span></div>
                <div class="progress-bar">
                    <div class="progress-fill {'green' if mem_info['ram']['percent'] < 30 else 'yellow' if mem_info['ram']['percent'] < 60 else 'orange' if mem_info['ram']['percent'] < 80 else 'red'}" style="width: {mem_info['ram']['percent']}%"></div>
                </div>
                <div class="stat-row"><span class="stat-label">Swap Total</span><span class="stat-value">{mem_info['swap']['total']}</span></div>
                <div class="stat-row"><span class="stat-label">Swap Used</span><span class="stat-value">{mem_info['swap']['used']}</span></div>
            </div>

            <div class="card">
                <h2>🌐 Network</h2>"""

    net = data["network"]
    html += f"""
                <div class="stat-row"><span class="stat-label">Bytes Sent</span><span class="stat-value">{format_bytes(net['bytes_sent'])}</span></div>
                <div class="stat-row"><span class="stat-label">Bytes Received</span><span class="stat-value">{format_bytes(net['bytes_recv'])}</span></div>
                <div class="stat-row"><span class="stat-label">Packets Sent</span><span class="stat-value">{net['packets_sent']:,}</span></div>
                <div class="stat-row"><span class="stat-label">Packets Received</span><span class="stat-value">{net['packets_recv']:,}</span></div>
            </div>

            <div class="card full">
                <h2>💾 Disk Partitions</h2>
                <table>
                    <tr><th>Device</th><th>Mount</th><th>FS</th><th>Total</th><th>Used</th><th>Free</th><th>Usage</th></tr>"""

    for disk in data["disks"]:
        color_class = 'green' if disk['percent'] < 30 else 'yellow' if disk['percent'] < 60 else 'orange' if disk['percent'] < 80 else 'red'
        html += f"""
                    <tr>
                        <td>{disk['device']}</td>
                        <td>{disk['mountpoint']}</td>
                        <td>{disk['fstype']}</td>
                        <td>{disk['total']}</td>
                        <td>{disk['used']}</td>
                        <td>{disk['free']}</td>
                        <td><div class="progress-bar"><div class="progress-fill {color_class}" style="width:{disk['percent']}%"></div></div> {disk['percent']}%</td>
                    </tr>"""

    html += """
                </table>
            </div>

            <div class="card full">
                <h2>⚡ Top Processes</h2>
                <table>
                    <tr><th>PID</th><th>Name</th><th>CPU %</th><th>MEM %</th><th>Status</th></tr>"""

    for proc in data["processes"]:
        html += f"""
                    <tr>
                        <td>{proc.get('pid', '?')}</td>
                        <td>{proc.get('name', 'unknown')}</td>
                        <td>{proc.get('cpu_percent', 0):.1f}%</td>
                        <td>{proc.get('memory_percent', 0):.1f}%</td>
                        <td>{proc.get('status', 'unknown')}</td>
                    </tr>"""

    html += f"""
                </table>
            </div>
        </div>

        <div class="footer">
            <p>Generated by <strong>SysView CLI</strong> v{__version__}</p>
        </div>
    </div>
</body>
</html>"""

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)

"""
Dashboard renderer using Rich library
Creates beautiful terminal UI for system monitoring
"""

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.layout import Layout
from rich.text import Text
from rich.progress_bar import ProgressBar
from rich.columns import Columns
from rich.align import Align
from rich import box

from . import __version__, __author__
from .system_info import (
    get_system_info,
    get_cpu_info,
    get_memory_info,
    get_disk_info,
    get_network_info,
    get_battery_info,
    get_temperature_info,
    format_bytes,
)


LOGO = r"""
  ____            __     ___               
 / ___| _   _ ___\ \   / (_) _____      __
 \___ \| | | / __| \ \ / /| |/ _ \ \ /\ / /
  ___) | |_| \__ \  \ V / | |  __/\ V  V / 
 |____/ \__, |___/   \_/  |_|\___| \_/\_/  
        |___/                    CLI v{}
""".format(__version__)


def get_usage_color(percent: float) -> str:
    """Return color based on usage percentage."""
    if percent < 30:
        return "green"
    elif percent < 60:
        return "yellow"
    elif percent < 80:
        return "dark_orange"
    else:
        return "red"


def make_progress_bar(percent: float, width: int = 30, label: str = "") -> Text:
    """Create a colored progress bar with text."""
    color = get_usage_color(percent)
    filled = int(width * percent / 100)
    empty = width - filled

    bar = Text()
    if label:
        bar.append(f"{label} ", style="bold white")
    bar.append("█" * filled, style=f"bold {color}")
    bar.append("░" * empty, style="dim white")
    bar.append(f" {percent:.1f}%", style=f"bold {color}")
    return bar


def render_header(console: Console) -> Panel:
    """Render the application header."""
    logo_text = Text(LOGO, style="bold cyan")
    subtitle = Text("System Resource Monitor", style="bold magenta", justify="center")

    header_content = Text()
    header_content.append_text(logo_text)
    header_content.append("\n")
    header_content.append_text(subtitle)

    return Panel(
        Align.center(header_content),
        border_style="bright_cyan",
        box=box.DOUBLE_EDGE,
    )


def render_system_info(console: Console) -> Panel:
    """Render system information panel."""
    info = get_system_info()

    table = Table(show_header=False, box=None, padding=(0, 2))
    table.add_column("Key", style="bold cyan", width=16)
    table.add_column("Value", style="white")

    table.add_row("🖥  Hostname", info["hostname"])
    table.add_row("🐧 OS", info["os"])
    table.add_row("🏗  Arch", info["architecture"])
    table.add_row("⚙  Processor", info["processor"][:45])
    table.add_row("🐍 Python", info["python_version"])
    table.add_row("🕐 Boot Time", info["boot_time"])
    table.add_row("⏱  Uptime", info["uptime"])

    return Panel(
        table,
        title="[bold bright_green]📋 System Information[/]",
        border_style="bright_green",
        box=box.ROUNDED,
    )


def render_cpu_info(console: Console) -> Panel:
    """Render CPU information panel."""
    info = get_cpu_info()

    content = Text()
    content.append(f"Physical Cores: ", style="bold cyan")
    content.append(f"{info['physical_cores']}  ", style="white")
    content.append(f"Logical Cores: ", style="bold cyan")
    content.append(f"{info['logical_cores']}  ", style="white")
    content.append(f"Freq: ", style="bold cyan")
    content.append(f"{info['current_frequency']}\n\n", style="white")

    # Overall CPU bar
    content.append_text(make_progress_bar(info["total_usage"], width=40, label="TOTAL"))
    content.append("\n\n")

    # Per-core bars
    for i, usage in enumerate(info["per_cpu_usage"]):
        label = f"Core {i:<2}"
        content.append_text(make_progress_bar(usage, width=25, label=label))
        if i < len(info["per_cpu_usage"]) - 1:
            content.append("\n")

    return Panel(
        content,
        title="[bold bright_yellow]🔥 CPU Usage[/]",
        border_style="bright_yellow",
        box=box.ROUNDED,
    )


def render_memory_info(console: Console) -> Panel:
    """Render memory information panel."""
    info = get_memory_info()

    content = Text()

    # RAM section
    content.append("━━━ RAM ━━━\n", style="bold bright_magenta")
    content.append(f"  Total:     {format_bytes(info['total'])}\n", style="white")
    content.append(f"  Used:      {format_bytes(info['used'])}\n", style="yellow")
    content.append(f"  Available: {format_bytes(info['available'])}\n\n", style="green")
    content.append_text(make_progress_bar(info["percent"], width=35, label="  RAM"))
    content.append("\n\n")

    # Swap section
    content.append("━━━ SWAP ━━━\n", style="bold bright_magenta")
    content.append(f"  Total: {format_bytes(info['swap_total'])}\n", style="white")
    content.append(f"  Used:  {format_bytes(info['swap_used'])}\n\n", style="yellow")
    content.append_text(make_progress_bar(info["swap_percent"], width=35, label="  SWAP"))

    return Panel(
        content,
        title="[bold bright_magenta]🧠 Memory[/]",
        border_style="bright_magenta",
        box=box.ROUNDED,
    )


def render_disk_info(console: Console) -> Panel:
    """Render disk information panel."""
    disks = get_disk_info()

    table = Table(box=box.SIMPLE_HEAVY, border_style="blue")
    table.add_column("Device", style="bold cyan", max_width=20)
    table.add_column("Mount", style="white", max_width=15)
    table.add_column("FS", style="dim", max_width=8)
    table.add_column("Total", style="white", justify="right")
    table.add_column("Used", style="yellow", justify="right")
    table.add_column("Free", style="green", justify="right")
    table.add_column("Usage", justify="center", min_width=20)

    for disk in disks:
        color = get_usage_color(disk["percent"])
        filled = int(15 * disk["percent"] / 100)
        empty = 15 - filled
        bar = f"[{color}]{'█' * filled}[/][dim]{'░' * empty}[/] [{color}]{disk['percent']:.0f}%[/]"

        table.add_row(
            disk["device"][:20],
            disk["mountpoint"][:15],
            disk["fstype"],
            format_bytes(disk["total"]),
            format_bytes(disk["used"]),
            format_bytes(disk["free"]),
            bar,
        )

    return Panel(
        table,
        title="[bold bright_blue]💾 Disk Partitions[/]",
        border_style="bright_blue",
        box=box.ROUNDED,
    )


def render_network_info(console: Console) -> Panel:
    """Render network information panel."""
    info = get_network_info()

    content = Text()
    content.append("━━━ Traffic Summary ━━━\n", style="bold bright_cyan")
    content.append(f"  ↑ Sent:     {format_bytes(info['bytes_sent'])}\n", style="green")
    content.append(f"  ↓ Received: {format_bytes(info['bytes_recv'])}\n", style="cyan")
    content.append(f"  📦 Packets: {info['packets_sent']:,} sent / {info['packets_recv']:,} recv\n\n", style="white")

    content.append("━━━ Interfaces ━━━\n", style="bold bright_cyan")
    for iface in info["interfaces"]:
        status = "[green]●[/green] UP" if iface["is_up"] else "[red]● DOWN[/red]"
        content.append(f"\n  {iface['name']}", style="bold white")
        content.append(f"  {status}")
        if iface["speed"] > 0:
            content.append(f"  ({iface['speed']} Mbps)", style="dim")
        content.append("\n")

        for addr in iface["addresses"]:
            content.append(f"    {addr['type']}: ", style="dim cyan")
            content.append(f"{addr['address']}\n", style="white")

    return Panel(
        content,
        title="[bold bright_cyan]🌐 Network[/]",
        border_style="bright_cyan",
        box=box.ROUNDED,
    )


def render_battery_and_temps(console: Console) -> Panel | None:
    """Render battery and temperature info."""
    battery = get_battery_info()
    temps = get_temperature_info()

    if not battery and not temps:
        return None

    content = Text()

    if battery:
        content.append("━━━ Battery ━━━\n", style="bold bright_green")
        plug_icon = "🔌" if battery["plugged"] else "🔋"
        content.append(f"  {plug_icon} Charge: ", style="white")
        color = get_usage_color(100 - battery["percent"])
        content.append(f"{battery['percent']}%\n", style=f"bold {color}")
        content.append_text(make_progress_bar(battery["percent"], width=30, label="  "))
        content.append(f"\n  Time: {battery['time_left']}\n", style="dim")

    if temps:
        content.append("\n━━━ Temperatures ━━━\n", style="bold bright_red")
        for sensor_name, entries in temps.items():
            for entry in entries[:3]:
                temp_color = "green" if entry.current < 60 else "yellow" if entry.current < 80 else "red"
                label = entry.label or sensor_name
                content.append(f"  🌡 {label[:20]}: ", style="white")
                content.append(f"{entry.current:.0f}°C", style=f"bold {temp_color}")
                if entry.high:
                    content.append(f" (max: {entry.high:.0f}°C)", style="dim")
                content.append("\n")

    return Panel(
        content,
        title="[bold bright_green]🔋 Battery & Sensors[/]",
        border_style="bright_green",
        box=box.ROUNDED,
    )


def render_dashboard():
    """Main function to render the complete dashboard."""
    console = Console()
    console.clear()

    # Header
    console.print(render_header(console))

    # System Info + CPU side by side (if terminal is wide enough)
    width = console.width
    if width >= 100:
        # Wide terminal: side-by-side layout
        cols = Columns(
            [render_system_info(console), render_cpu_info(console)],
            equal=True,
            expand=True,
        )
        console.print(cols)
    else:
        console.print(render_system_info(console))
        console.print(render_cpu_info(console))

    # Memory
    console.print(render_memory_info(console))

    # Disks
    console.print(render_disk_info(console))

    # Network
    console.print(render_network_info(console))

    # Battery & Temps (if available)
    battery_panel = render_battery_and_temps(console)
    if battery_panel:
        console.print(battery_panel)

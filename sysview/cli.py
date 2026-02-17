"""
SysView CLI - Main entry point
"""

import argparse
import sys
import time
import json

from rich.console import Console
from rich.live import Live
from rich.text import Text

from . import __version__
from .dashboard import render_dashboard
from .system_info import format_bytes
from .export import export_json, export_html


def print_banner():
    """Print a startup banner."""
    console = Console()
    banner = Text()
    banner.append("\n  ⚡ ", style="bold yellow")
    banner.append("SysView CLI", style="bold bright_cyan")
    banner.append(f" v{__version__}", style="dim cyan")
    banner.append(" - System Resource Monitor\n", style="white")
    console.print(banner)


def run_once():
    """Run the dashboard once and exit."""
    render_dashboard()


def run_live(interval: float = 2.0):
    """Run the dashboard with live updates."""
    console = Console()
    console.clear()

    try:
        while True:
            render_dashboard()
            console.print(
                f"\n  [dim]Refreshing every {interval}s... Press Ctrl+C to exit[/]"
            )
            time.sleep(interval)
            console.clear()
    except KeyboardInterrupt:
        console.print("\n  [bold green]👋 Goodbye![/]\n")
        sys.exit(0)


def run_json():
    """Output system info as JSON."""
    data = export_json()
    print(json.dumps(data, indent=2, default=str))


def run_export_html(output_path: str):
    """Export system info as HTML report."""
    export_html(output_path)
    console = Console()
    console.print(f"\n  [bold green]✅ Report saved to: {output_path}[/]\n")


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        prog="sysview",
        description="🖥  SysView CLI - Beautiful Terminal System Monitor",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  sysview                    Show system dashboard (single snapshot)
  sysview --live             Live monitoring mode (auto-refresh)
  sysview --live -i 5        Live mode, refresh every 5 seconds
  sysview --json             Output as JSON
  sysview --html report.html Export as HTML report

Made with ❤ by for-test0x
        """,
    )

    parser.add_argument(
        "-v", "--version",
        action="version",
        version=f"%(prog)s {__version__}",
    )

    parser.add_argument(
        "--live", "-l",
        action="store_true",
        help="Enable live monitoring mode with auto-refresh",
    )

    parser.add_argument(
        "--interval", "-i",
        type=float,
        default=2.0,
        help="Refresh interval in seconds for live mode (default: 2.0)",
    )

    parser.add_argument(
        "--json", "-j",
        action="store_true",
        help="Output system information as JSON",
    )

    parser.add_argument(
        "--html",
        type=str,
        metavar="FILE",
        help="Export system report as HTML file",
    )

    parser.add_argument(
        "--no-color",
        action="store_true",
        help="Disable colored output",
    )

    args = parser.parse_args()

    if args.no_color:
        import os
        os.environ["NO_COLOR"] = "1"

    if args.json:
        run_json()
    elif args.html:
        run_export_html(args.html)
    elif args.live:
        print_banner()
        run_live(interval=args.interval)
    else:
        run_once()


if __name__ == "__main__":
    main()

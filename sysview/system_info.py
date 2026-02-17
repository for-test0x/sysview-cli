"""
System information gathering utilities
"""

import platform
import socket
import os
import datetime
from typing import Dict, Any, List, Optional

import psutil


def get_system_info() -> Dict[str, Any]:
    """Get general system information."""
    uname = platform.uname()
    boot_time = datetime.datetime.fromtimestamp(psutil.boot_time())
    uptime = datetime.datetime.now() - boot_time

    hours, remainder = divmod(int(uptime.total_seconds()), 3600)
    minutes, seconds = divmod(remainder, 60)
    days, hours = divmod(hours, 24)

    uptime_str = ""
    if days > 0:
        uptime_str += f"{days}d "
    uptime_str += f"{hours}h {minutes}m {seconds}s"

    return {
        "hostname": uname.node,
        "os": f"{uname.system} {uname.release}",
        "os_version": uname.version,
        "architecture": uname.machine,
        "processor": uname.processor or platform.processor() or "Unknown",
        "python_version": platform.python_version(),
        "boot_time": boot_time.strftime("%Y-%m-%d %H:%M:%S"),
        "uptime": uptime_str,
    }


def get_cpu_info() -> Dict[str, Any]:
    """Get CPU information and usage."""
    cpu_freq = psutil.cpu_freq()
    per_cpu = psutil.cpu_percent(interval=0.5, percpu=True)

    return {
        "physical_cores": psutil.cpu_count(logical=False) or 0,
        "logical_cores": psutil.cpu_count(logical=True) or 0,
        "max_frequency": f"{cpu_freq.max:.0f} MHz" if cpu_freq else "N/A",
        "current_frequency": f"{cpu_freq.current:.0f} MHz" if cpu_freq else "N/A",
        "total_usage": psutil.cpu_percent(interval=0),
        "per_cpu_usage": per_cpu,
    }


def get_memory_info() -> Dict[str, Any]:
    """Get RAM information."""
    mem = psutil.virtual_memory()
    swap = psutil.swap_memory()

    return {
        "total": mem.total,
        "available": mem.available,
        "used": mem.used,
        "percent": mem.percent,
        "swap_total": swap.total,
        "swap_used": swap.used,
        "swap_percent": swap.percent,
    }


def get_disk_info() -> List[Dict[str, Any]]:
    """Get disk partition information."""
    disks = []
    partitions = psutil.disk_partitions()

    for partition in partitions:
        try:
            usage = psutil.disk_usage(partition.mountpoint)
            disks.append({
                "device": partition.device,
                "mountpoint": partition.mountpoint,
                "fstype": partition.fstype,
                "total": usage.total,
                "used": usage.used,
                "free": usage.free,
                "percent": usage.percent,
            })
        except PermissionError:
            continue

    return disks


def get_network_info() -> Dict[str, Any]:
    """Get network information."""
    net_io = psutil.net_io_counters()
    interfaces = []

    addrs = psutil.net_if_addrs()
    stats = psutil.net_if_stats()

    for iface_name, iface_addrs in addrs.items():
        iface_info = {
            "name": iface_name,
            "is_up": stats[iface_name].isup if iface_name in stats else False,
            "speed": stats[iface_name].speed if iface_name in stats else 0,
            "addresses": [],
        }
        for addr in iface_addrs:
            if addr.family == socket.AF_INET:
                iface_info["addresses"].append({
                    "type": "IPv4",
                    "address": addr.address,
                    "netmask": addr.netmask,
                })
            elif addr.family == socket.AF_INET6:
                iface_info["addresses"].append({
                    "type": "IPv6",
                    "address": addr.address,
                })

        interfaces.append(iface_info)

    return {
        "bytes_sent": net_io.bytes_sent,
        "bytes_recv": net_io.bytes_recv,
        "packets_sent": net_io.packets_sent,
        "packets_recv": net_io.packets_recv,
        "interfaces": interfaces,
    }


def get_process_info(top_n: int = 10) -> List[Dict[str, Any]]:
    """Get top processes by CPU and memory usage."""
    processes = []
    for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent', 'status']):
        try:
            info = proc.info
            processes.append(info)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue

    processes.sort(key=lambda x: x.get('cpu_percent', 0) or 0, reverse=True)
    return processes[:top_n]


def get_battery_info() -> Optional[Dict[str, Any]]:
    """Get battery info if available."""
    try:
        battery = psutil.sensors_battery()
        if battery:
            return {
                "percent": battery.percent,
                "plugged": battery.power_plugged,
                "time_left": str(datetime.timedelta(seconds=battery.secsleft)) if battery.secsleft != psutil.POWER_TIME_UNLIMITED and battery.secsleft != psutil.POWER_TIME_UNKNOWN else ("Charging" if battery.power_plugged else "Unknown"),
            }
    except Exception:
        pass
    return None


def get_temperature_info() -> Optional[Dict[str, List]]:
    """Get temperature sensors if available."""
    try:
        temps = psutil.sensors_temperatures()
        if temps:
            return temps
    except (AttributeError, Exception):
        pass
    return None


def format_bytes(bytes_val: int) -> str:
    """Format bytes to human readable string."""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if bytes_val < 1024.0:
            return f"{bytes_val:.1f} {unit}"
        bytes_val /= 1024.0
    return f"{bytes_val:.1f} PB"

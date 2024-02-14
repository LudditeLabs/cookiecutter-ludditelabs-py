from pathlib import Path

import psutil


def get_process_cmd() -> str:  # pragma: no cover
    """Get the current process command line."""
    cmd = psutil.Process().cmdline()
    if Path(cmd[0]).stem.startswith("python"):
        cmd.pop(0)
    cmd[0] = Path(cmd[0]).name
    return " ".join(cmd)

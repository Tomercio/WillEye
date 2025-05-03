import subprocess


def scan(target: str, stype: str, ports: str) -> str:
    """
    Run nmap scan. Requires nmap in your PATH.
    """
    if not target:
        raise ValueError("nmap_adapter.scan: target is empty")
    cmd = ["nmap", stype, "-p", ports, target]
    try:
        return subprocess.check_output(cmd, text=True)
    except FileNotFoundError:
        raise RuntimeError(
            "Command not found: 'nmap'.\n"
            "Please install Nmap and ensure 'nmap' is in your PATH."
        )

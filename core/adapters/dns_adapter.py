import subprocess


def dig(target: str) -> str:
    """
    Perform a DNS lookup via 'dig'.
    """
    if not target:
        raise ValueError("dns_adapter.dig: target is empty")
    cmd = ["dig", "+noall", "+answer", target]
    try:
        return subprocess.check_output(cmd, text=True)
    except FileNotFoundError:
        raise RuntimeError(
            "Command not found: 'dig'.\n"
            "Please install a DNS client (e.g. bind-tools on Linux)\n"
            "or use WSL / Git Bash on Windows."
        )


def subdomains(target: str) -> str:
    """
    Discover subdomains via 'subfinder'.
    """
    if not target:
        raise ValueError("dns_adapter.subdomains: target is empty")
    cmd = ["subfinder", "-d", target]
    try:
        return subprocess.check_output(cmd, text=True)
    except FileNotFoundError:
        raise RuntimeError(
            "Command not found: 'subfinder'.\n"
            "Install Subfinder (https://github.com/projectdiscovery/subfinder)\n"
            "and ensure it's in your PATH."
        )

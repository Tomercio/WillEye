import subprocess


def lookup(target: str) -> str:
    """
    Perform a WHOIS lookup. On Windows you’ll need a 'whois' binary in PATH.
    """
    if not target:
        raise ValueError("whois_adapter.lookup: target is empty")
    cmd = ["whois", target]
    try:
        return subprocess.check_output(cmd, text=True)
    except FileNotFoundError:
        raise RuntimeError(
            "Command not found: 'whois'.\n"
            "Please install a WHOIS client (e.g. 'choco install whois')\n"
            "or add it to your PATH."
        )

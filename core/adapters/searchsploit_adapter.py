import subprocess


def search(term: str) -> str:
    """
    Run SearchSploit. Requires exploit-db's 'searchsploit' script in PATH.
    """
    if not term:
        raise ValueError("searchsploit_adapter.search: term is empty")
    cmd = ["searchsploit", term]
    try:
        return subprocess.check_output(cmd, text=True)
    except FileNotFoundError:
        raise RuntimeError(
            "Command not found: 'searchsploit'.\n"
            "Install exploit-db (searchsploit) and add it to your PATH."
        )

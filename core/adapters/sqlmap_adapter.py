import subprocess


def sqlmap_scan(url: str, param: str = None, level: int = 1, risk: int = 1) -> str:
    """
    Run sqlmap against the given URL (optionally target a single parameter).
    """
    if not url:
        raise ValueError("sqlmap_adapter: URL is required")
    cmd = [
        "sqlmap",
        "-u", url,
        "--batch",
        f"--level={level}",
        f"--risk={risk}"
    ]
    if param:
        cmd += ["-p", param]
    try:
        return subprocess.check_output(cmd, text=True, stderr=subprocess.STDOUT)
    except FileNotFoundError:
        raise RuntimeError(
            "sqlmap not found; please install and add to your PATH")
    except subprocess.CalledProcessError as e:
        return e.output

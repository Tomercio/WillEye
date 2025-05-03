import subprocess


def xss_scan(url: str, param: str = None) -> str:
    """
    Run XSStrike against the given URL to detect XSS.
    """
    if not url:
        raise ValueError("xss_adapter: URL is required")
    cmd = ["xsstrike", "-u", url, "--crawl"]
    if param:
        cmd += ["--param", param]
    try:
        return subprocess.check_output(cmd, text=True, stderr=subprocess.STDOUT)
    except FileNotFoundError:
        raise RuntimeError(
            "XSStrike not found; pip install xsstrike and add to PATH")
    except subprocess.CalledProcessError as e:
        return e.output

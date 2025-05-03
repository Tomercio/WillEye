import subprocess


def lookup(target: str) -> str:
    if not target:
        raise ValueError("whois_adapter: target is empty")
    cmd = ["whois", target]
    try:
        return subprocess.check_output(cmd, text=True)
    except FileNotFoundError:
        raise RuntimeError("Install 'whois' and ensure it's in your PATH")
    except subprocess.CalledProcessError as e:
        return e.output

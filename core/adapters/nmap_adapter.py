import subprocess


def scan(target: str, flags: str, ports: str) -> str:
    if not target:
        raise ValueError("nmap_adapter.scan: target is empty")
    cmd = ["nmap"] + flags.split() + ["-p", ports, target]
    try:
        return subprocess.check_output(cmd, text=True)
    except FileNotFoundError:
        raise RuntimeError("Install 'nmap' and ensure it's in your PATH")
    except subprocess.CalledProcessError as e:
        return e.output

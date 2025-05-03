import subprocess


def dig(target: str) -> str:
    if not target:
        raise ValueError("dns_adapter.dig: target is empty")
    cmd = ["dig", "+noall", "+answer", target]
    try:
        return subprocess.check_output(cmd, text=True)
    except FileNotFoundError:
        raise RuntimeError("Install 'dnsutils' (dig) in your PATH")
    except subprocess.CalledProcessError as e:
        return e.output


def subdomains(target: str) -> str:
    if not target:
        raise ValueError("dns_adapter.subdomains: target is empty")
    cmd = ["subfinder", "-d", target]
    try:
        return subprocess.check_output(cmd, text=True)
    except FileNotFoundError:
        raise RuntimeError("Install 'subfinder' and add it to PATH")
    except subprocess.CalledProcessError as e:
        return e.output

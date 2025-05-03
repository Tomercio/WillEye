import subprocess
from typing import List


def zap_baseline(target: str, rules_file: str = None) -> str:
    if not target:
        raise ValueError("webapp_adapter.zap_baseline: target empty")
    cmd = ["zap-baseline.py", "-t", target, "-r", "zap_report.html"]
    if rules_file:
        cmd += ["-z", f"-configfile={rules_file}"]
    try:
        return subprocess.check_output(cmd, text=True, stderr=subprocess.STDOUT)
    except FileNotFoundError:
        raise RuntimeError(
            "Install OWASP ZAP CLI and add zap-baseline.py to PATH")
    except subprocess.CalledProcessError as e:
        return e.output


def dir_bruteforce(target: str, wordlists: List[str] = None, extensions: List[str] = None) -> str:
    if not target:
        raise ValueError("webapp_adapter.dir_bruteforce: target empty")
    wordlists = wordlists or [
        "/usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt"]
    extensions = extensions or []
    out = ""
    for wl in wordlists:
        cmd = ["gobuster", "dir", "-u", target, "-w", wl]
        if extensions:
            cmd += ["-x", ",".join(extensions)]
        try:
            res = subprocess.check_output(cmd, text=True)
            out += f"\n-- Results for {wl} --\n{res}"
        except FileNotFoundError:
            raise RuntimeError("Install 'gobuster' and ensure it's in PATH")
        except subprocess.CalledProcessError as e:
            out += f"\n-- Gobuster error on {wl}: {e.returncode}"
    return out

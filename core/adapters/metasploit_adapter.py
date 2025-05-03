import subprocess


def exploit(target: str, module: str) -> str:
    if not target or not module:
        raise ValueError("metasploit_adapter: missing target or module")
    cmd = [
        "msfconsole", "-q",
        "-x", f"use {module}; set RHOST {target}; run; exit"
    ]
    try:
        return subprocess.check_output(cmd, text=True)
    except FileNotFoundError:
        raise RuntimeError(
            "Install Metasploit and ensure 'msfconsole' in PATH")
    except subprocess.CalledProcessError as e:
        return e.output

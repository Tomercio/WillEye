# core/adapters/priv_esc_adapter.py

import subprocess
import time

# wrap optional imports so missing libs don’t error out at import time
try:
    import telnetlib  # type: ignore[reportMissingImports]
except ImportError:
    telnetlib = None

try:
    import winrm      # type: ignore[reportMissingImports]
except ImportError:
    winrm = None


def run_linpeas_ssh(target: str, user: str,
                    keyfile: str = None,
                    password: str = None) -> str:
    """
    Copy linpeas.sh to the target and run it via SSH.
    If no keyfile is provided, uses sshpass + password.
    """
    if password and not keyfile:
        scp_cmd = ["sshpass", "-p", password,
                   "scp", "-o", "StrictHostKeyChecking=no"]
    else:
        scp_cmd = ["scp", "-o", "StrictHostKeyChecking=no"]
        if keyfile:
            scp_cmd += ["-i", keyfile]
    scp_cmd += ["/usr/local/bin/linpeas.sh",
                f"{user}@{target}:/tmp/linpeas.sh"]

    try:
        subprocess.check_output(scp_cmd, stderr=subprocess.STDOUT, text=True)
    except Exception as e:
        return f"[SCP Error]\n{e}"

    if password and not keyfile:
        ssh_cmd = ["sshpass", "-p", password,
                   "ssh", "-o", "StrictHostKeyChecking=no"]
    else:
        ssh_cmd = ["ssh", "-o", "StrictHostKeyChecking=no"]
        if keyfile:
            ssh_cmd += ["-i", keyfile]
    ssh_cmd += [f"{user}@{target}",
                "bash /tmp/linpeas.sh; rm /tmp/linpeas.sh"]

    try:
        out = subprocess.check_output(ssh_cmd,
                                      stderr=subprocess.STDOUT,
                                      text=True)
    except Exception as e:
        return f"[SSH Error]\n{e}"

    return out


def run_linpeas_telnet(target: str, user: str,
                       password: str, port: int = 23) -> str:
    """
    Execute linpeas.sh via Telnet (assumes it's already on /tmp).
    """
    if telnetlib is None:
        return "Telnet support not available: telnetlib not installed."

    try:
        tn = telnetlib.Telnet(target, port, timeout=10)
        tn.read_until(b"login: ")
        tn.write(user.encode() + b"\n")
        tn.read_until(b"Password: ")
        tn.write(password.encode() + b"\n")
        tn.write(b"bash /tmp/linpeas.sh; rm /tmp/linpeas.sh\n")
        tn.write(b"exit\n")
        output = tn.read_all().decode('ascii', errors='ignore')
        return output
    except Exception as e:
        return f"[Telnet Error]\n{e}"


def run_linpeas_winrm(target: str, user: str,
                      password: str, port: int = 5985) -> str:
    """
    Execute linPEAS via WinRM. Requires pywinrm.
    """
    if winrm is None:
        return "WinRM support not available: pywinrm not installed."

    session = winrm.Session(f'http://{target}:{port}/wsman',
                            auth=(user, password))
    r = session.run_cmd('powershell.exe',
                        ['-ExecutionPolicy', 'Bypass', '-File', 'C:\\linPEAS.ps1'])
    return r.std_out.decode() + r.std_err.decode()


def run_linpeas(target: str,
                user: str,
                method: str = 'ssh',
                keyfile: str = None,
                password: str = None,
                port: int = None) -> str:
    """
    Dispatch to the chosen protocol:
      - 'ssh'
      - 'telnet'
      - 'winrm'
    """
    if method == 'ssh':
        return run_linpeas_ssh(target, user, keyfile, password)
    elif method == 'telnet':
        return run_linpeas_telnet(target, user, password, port or 23)
    elif method == 'winrm':
        return run_linpeas_winrm(target, user, password, port or 5985)
    else:
        return f"Unsupported method: {method}"

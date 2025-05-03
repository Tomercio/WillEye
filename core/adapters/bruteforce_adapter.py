import subprocess


def ssh_bruteforce(target: str, user: str, passlist: str, threads: int = 4) -> str:
    if not (target and user and passlist):
        raise ValueError(
            "bruteforce_adapter.ssh_bruteforce: missing arguments")
    cmd = ["hydra", "-l", user, "-P", passlist,
           "-t", str(threads), "ssh://" + target]
    try:
        return subprocess.check_output(cmd, text=True)
    except FileNotFoundError:
        raise RuntimeError("Install 'hydra' and ensure it's in PATH")
    except subprocess.CalledProcessError as e:
        return e.output

import subprocess


def run_linpeas(path: str = "/usr/local/bin/linpeas.sh") -> str:
    try:
        return subprocess.check_output([path], text=True, stderr=subprocess.STDOUT, timeout=300)
    except FileNotFoundError:
        raise RuntimeError("Download 'linpeas.sh' and place it in your PATH")
    except subprocess.CalledProcessError as e:
        return e.output
    except subprocess.TimeoutExpired:
        return "linPEAS timed out (300s)"

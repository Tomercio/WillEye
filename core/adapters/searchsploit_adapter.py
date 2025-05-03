import subprocess


def search(term: str) -> str:
    if not term:
        raise ValueError("searchsploit_adapter: term is empty")
    cmd = ["searchsploit", term]
    try:
        return subprocess.check_output(cmd, text=True)
    except FileNotFoundError:
        raise RuntimeError("Install 'searchsploit' (exploit-db) in your PATH")
    except subprocess.CalledProcessError as e:
        return e.output

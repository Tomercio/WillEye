import subprocess


def api_fuzz(target: str, endpoints: str = "/usr/share/wordlists/api-endpoints.txt", threads: int = 50) -> str:
    if not target:
        raise ValueError("api_cloud_adapter: target empty")
    cmd = [
        "ffuf",
        "-u", f"{target}/FUZZ",
        "-w", endpoints,
        "-t", str(threads),
        "-mc", "200,301,302"
    ]
    try:
        return subprocess.check_output(cmd, text=True)
    except FileNotFoundError:
        raise RuntimeError("Install 'ffuf' and ensure it's in PATH")
    except subprocess.CalledProcessError as e:
        return e.output

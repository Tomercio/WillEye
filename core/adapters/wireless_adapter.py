import subprocess
import time
import shlex


def wireless_tests(interface: str = "wlan0", duration: int = 10) -> str:
    """
    Wireless & MITM enumeration:
      1. List wireless interfaces via `iwconfig`
      2. Start monitor mode on the chosen interface (`airmon-ng`)
      3. Run `airodump-ng` for a few seconds to capture nearby networks/clients
      4. Stop monitor mode
      5. (Optional) Quick MITM sniff with Bettercap
    Requires: airmon-ng, airodump-ng (aircrack-ng), bettercap
    """
    results = []

    try:
        out = subprocess.check_output(
            ["iwconfig"], text=True, stderr=subprocess.DEVNULL)
        results.append("=== iwconfig (wireless interfaces) ===")
        results.append(out)
    except FileNotFoundError:
        results.append("ERROR: iwconfig not found (install wireless-tools).")

    mon_iface = f"{interface}mon"

    try:
        results.append(f"=== airmon-ng start {interface} ===")
        out = subprocess.check_output(
            ["airmon-ng", "start", interface],
            text=True, stderr=subprocess.STDOUT
        )
        results.append(out)
    except FileNotFoundError:
        results.append("ERROR: airmon-ng not found (install aircrack-ng).")
        return "\n".join(results)
    except subprocess.CalledProcessError as e:
        results.append(f"[airmon-ng error {e.returncode}]\n{e.output}")

    try:
        results.append(f"=== airodump-ng on {mon_iface} for {duration}s ===")
        proc = subprocess.Popen(
            ["airodump-ng", mon_iface],
            stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
            text=True
        )
        time.sleep(duration)
        proc.terminate()
        out, _ = proc.communicate(timeout=5)
        results.append(out)
    except FileNotFoundError:
        results.append("ERROR: airodump-ng not found (install aircrack-ng).")
    except Exception as e:
        results.append(f"[airodump-ng error] {e}")

    try:
        results.append(f"=== airmon-ng stop {mon_iface} ===")
        out = subprocess.check_output(
            ["airmon-ng", "stop", mon_iface],
            text=True, stderr=subprocess.STDOUT
        )
        results.append(out)
    except FileNotFoundError:
        results.append("ERROR: airmon-ng not found for stopping monitor.")
    except subprocess.CalledProcessError as e:
        results.append(f"[airmon-ng stop error {e.returncode}]\n{e.output}")

    try:
        results.append("=== bettercap sniff (5s) ===")
        cmd = f"bettercap -iface {interface} --eval 'net.recon on; net.sniff on; sleep 5; net.sniff off; net.recon off; exit'"
        out = subprocess.check_output(shlex.split(
            cmd), text=True, stderr=subprocess.STDOUT)
        results.append(out)
    except FileNotFoundError:
        results.append("ERROR: bettercap not found (install bettercap).")
    except subprocess.CalledProcessError as e:
        results.append(f"[bettercap error {e.returncode}]\n{e.output}")

    return "\n".join(results)

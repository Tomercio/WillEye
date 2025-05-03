#!/usr/bin/env python3
from core.engine import Engine
import os
import sys
import socket
from urllib.parse import urlparse

# ensure the script’s own folder is on sys.path so core/ is importable
sys.path.insert(0, os.path.dirname(__file__))


# ASCII art banner
BANNER = r"""
┌───────────────────────────────────────────────────────────────────────┐
│                               Will Eye
└───────────────────────────────────────────────────────────────────────┘
   ____            _             _    _____       _ _     _           
  |  _ \ ___  __ _| |_ ___  _ __| |_ | ____|_ __ (_) | __| | ___ _ __ 
  | |_) / _ \/ _` | __/ _ \| '__| __||  _| | '_ \| | |/ _` |/ _ \ '__|
  |  __/  __/ (_| | || (_) | |  | |_ | |___| | | | | | (_| |  __/ |   
  |_|   \___|\__,_|\__\___/|_|   \__||_____|_| |_|_|_|\__,_|\___|_|   

                          Learn ethical hacking step by step
"""

WARNING = (
    "WARNING: This tool is for educational purposes only. Always ensure you have proper\n"
    "authorization before testing any system or network. Unauthorized testing is illegal."
)

STEPS = [
    "Target Setup",
    "Information Gathering",
    "Port Scanning",
    "Service Enumeration",
    "Vulnerability Detection",
    "Exploitation",
    "Reporting"
]


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


def print_ui(statuses):
    clear_screen()
    print(BANNER)
    print("\n" + WARNING + "\n")
    # table header
    print(f"{' Penetration Testing Workflow ':─^65}")
    print(f"| {'Step':<30} | {'Status':<10} |")
    print(f"{'-'*3}+{'-'*32}+{'-'*12}")
    for step, stat in zip(STEPS, statuses):
        print(f"| {step:<30} | {stat:<10} |")
    print(f"{'-'*3}+{'-'*32}+{'-'*12}\n")
    # menu
    print("Menu Options:")
    for i, step in enumerate(STEPS, 1):
        print(f"  {i}. {step}")
    print("  0. Exit\n")


def pause():
    input("\nPress Enter to continue...")


def step_target(engine, statuses):
    raw = input("Enter domain or IP (you can include https://): ").strip()
    # allow full URLs or bare hostnames
    parsed = urlparse(raw if "://" in raw else "//" + raw)
    host = parsed.netloc or parsed.path

    try:
        resolved = socket.gethostbyname(host)
    except Exception as e:
        print(f"✗ Could not resolve {host}: {e}")
        pause()
        return

    engine.target = host
    print(f"✓ Target set to {host} ({resolved})")
    statuses[0] = "Done"
    pause()


def step_info(engine, statuses):
    if not engine.target:
        print("⚠️  Please set the target first (option 1).")
        pause()
        return

    print("→ WHOIS lookup:")
    try:
        out = engine.run_whois()
        print(out)
    except Exception as e:
        print(f"Error: {e}")

    print("\n→ DNS enumeration:")
    try:
        out = engine.run_dns_enum()
        print(out)
    except Exception as e:
        print(f"Error: {e}")

    print("\n→ Subdomain discovery:")
    try:
        out = engine.run_subdomains()
        print(out)
    except Exception as e:
        print(f"Error: {e}")

    statuses[1] = "Done"
    pause()


def step_scan(engine, statuses):
    if not engine.target:
        print("⚠️  Please set the target first (option 1).")
        pause()
        return

    stype = input("Scan type   (e.g. -sS): ").strip() or "-sS"
    ports = input("Port range  (e.g. 1-1024): ").strip() or "1-1024"
    print(f"\n→ Running nmap {stype} -p {ports} {engine.target} …\n")
    try:
        out = engine.run_nmap(stype, ports)
        print(out)
    except Exception as e:
        print(f"Error: {e}")

    statuses[2] = "Done"
    pause()


def step_enum_services(engine, statuses):
    print("Service enumeration is not yet implemented.")
    statuses[3] = "Done"
    pause()


def step_vuln_detect(engine, statuses):
    print("Vulnerability detection is not yet implemented.")
    statuses[4] = "Done"
    pause()


def step_exploitation(engine, statuses):
    print("Exploitation is not yet implemented.")
    statuses[5] = "Done"
    pause()


def step_reporting(engine, statuses):
    fname = input("Report filename [report.txt]: ").strip() or "report.txt"
    try:
        engine.write_report(fname)
        print(f"✓ Report saved to {fname}")
    except Exception as e:
        print(f"Error writing report: {e}")
    statuses[6] = "Done"
    pause()


def main():
    engine = Engine()
    statuses = ["Pending"] * len(STEPS)

    actions = {
        "1": step_target,
        "2": step_info,
        "3": step_scan,
        "4": step_enum_services,
        "5": step_vuln_detect,
        "6": step_exploitation,
        "7": step_reporting,
    }

    while True:
        print_ui(statuses)
        choice = input("Select an option: ").strip()
        if choice == "0":
            print("Bye!")
            sys.exit(0)
        action = actions.get(choice)
        if action:
            action(engine, statuses)
        else:
            print("Invalid option.")
            pause()


if __name__ == "__main__":
    main()

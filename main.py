from core.engine import Engine
import os
import sys
import socket
from urllib.parse import urlparse

sys.path.insert(0, os.path.dirname(__file__))


BANNER = r"""
┌───────────────────────────────────────────────────────────────────────────┐
│                                 WillEye                                 │
└───────────────────────────────────────────────────────────────────────────┘
"""

WARNING = (
    "WARNING: Educational use only. Obtain authorization before testing any system.\n"
    "Unauthorized testing is illegal."
)

STEPS = [
    "Target Setup",  # 1
    "Information Gathering",  # 2
    "Port Scanning",  # 3
    "Service Enumeration",  # 4
    "Vulnerability Detection",  # 5
    "Exploitation",  # 6
    "Web App Testing",  # 7
    "Brute-Force & Credentials",  # 8
    "Post-Exploitation",  # 9
    "Privilege Escalation",  # 10
    "Wireless & MITM",  # 11
    "API/Cloud Scanning",  # 12
    "Remediation & Retest",  # 13
    "SQL Injection Testing",  # 14
    "XSS Testing",  # 15
    "Reporting"  # 16
]


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


def show_welcome():
    clear_screen()
    print("Welcome to WillEye!\n")
    print("An interactive penetration testing framework — walk through each phase")
    print("from reconnaissance to remediation in a single CLI.\n")
    print("Before you begin, make sure you have these tools installed and in your PATH:")
    tools = [
        "whois", "dig", "subfinder", "nmap", "searchsploit",
        "msfconsole", "zap-baseline.py", "gobuster", "hydra",
        "linpeas.sh", "airodump-ng", "bettercap", "ffuf",
        "sqlmap", "xsstrike"
    ]
    for t in tools:
        print(f"  • {t}")
    input("\nPress Enter to continue to the main menu…")


def print_ui(statuses):
    clear_screen()
    print(BANNER)
    print(WARNING + "\n")
    # Header
    print(f"{' PenTest Workflow ':─^75}")
    print(f"| {'Step':<30} | {'Status':<12} |")
    print(f"{'-'*3}+{'-'*32}+{'-'*14}")
    for step, stat in zip(STEPS, statuses):
        print(f"| {step:<30} | {stat:<12} |")
    print(f"{'-'*3}+{'-'*32}+{'-'*14}\n")
    # Menu
    for i, step in enumerate(STEPS, 1):
        print(f"  {i}. {step}")
    print("  0. Exit\n")


def pause():
    input("Press Enter to continue...")


def step_target(engine, stats):
    raw = input("Enter domain or IP: ").strip()
    parsed = urlparse(raw if "://" in raw else "//"+raw)
    host = parsed.netloc or parsed.path
    try:
        ip = socket.gethostbyname(host)
        engine.target = host
        print(f"✓ Target set to {host} ({ip})")
        stats[0] = "Done"
    except Exception as e:
        print(f"✗ Could not resolve target: {e}")
    pause()


def step_info(engine, stats):
    if not engine.target:
        print("⚠️  Set a target first (step 1).")
        pause()
        return
    print("→ WHOIS lookup:")
    print(engine.run_whois())
    print("\n→ DNS enumeration:")
    print(engine.run_dns_enum())
    print("\n→ Subdomain discovery:")
    print(engine.run_subdomains())
    stats[1] = "Done"
    pause()


def step_scan(engine, stats):
    if not engine.target:
        print("⚠️  Set a target first (step 1).")
        pause()
        return
    nmap_flags = input(
        "Enter Nmap flags (e.g. -sS -sV -Pn) [default -sS]: ").strip() or "-sS"
    ports = input("Enter port range [default 1-1024]: ").strip() or "1-1024"
    print(f"→ Running nmap {nmap_flags} -p {ports} {engine.target}\n")
    print(engine.run_nmap(nmap_flags, ports))
    stats[2] = "Done"
    pause()


def step_service(engine, stats):
    print("→ Service Enumeration (-sV -sC):")
    print(engine.run_service_enum())
    stats[3] = "Done"
    pause()


def step_vuln(engine, stats):
    term = input("Enter search term for vulnerabilities: ").strip()
    print(f"→ SearchSploit for '{term}':")
    print(engine.run_searchsploit(term))
    stats[4] = "Done"
    pause()


def step_exploit(engine, stats):
    module = input("Enter Metasploit module path: ").strip()
    print(f"→ Running exploit {module}:")
    try:
        print(engine.run_exploit(module))
    except Exception as e:
        print(f"✗ Exploitation error: {e}")
    stats[5] = "Done"
    pause()


def step_webapp(engine, stats):
    print("→ OWASP ZAP Baseline + Directory Bruteforce:")
    print(engine.run_webapp_tests())
    stats[6] = "Done"
    pause()


def step_bruteforce(engine, stats):
    user = input("Enter SSH username: ").strip()
    pwlist = input("Enter password list path: ").strip()
    print(f"→ Running SSH brute-force as {user}:")
    print(engine.run_bruteforce(user, pwlist))
    stats[7] = "Done"
    pause()


def step_postex(engine, stats):
    print("→ Post-Exploitation Enumeration:")
    print(engine.run_post_exploit())
    stats[8] = "Done"
    pause()


def step_privesc(engine, stats):
    print("→ Privilege Escalation Checks (linPEAS):")
    print(engine.run_priv_esc())
    stats[9] = "Done"
    pause()


def step_wireless(engine, stats):
    print("→ Wireless & MITM Tests:")
    print(engine.run_wireless())
    stats[10] = "Done"
    pause()


def step_apicloud(engine, stats):
    print("→ API / Cloud Fuzzing (ffuf):")
    print(engine.run_api_cloud())
    stats[11] = "Done"
    pause()


def step_remed(engine, stats):
    print("→ Generating Remediation Guide:")
    print(engine.run_remediation())
    stats[12] = "Done"
    pause()


def step_sqlmap(engine, stats):
    url = input("Enter URL for SQLi testing: ").strip()
    param = input(" Parameter to test (e.g. id) [optional]: ").strip() or None
    print(f"→ Running sqlmap on {url} (param={param}) …\n")
    print(engine.run_sqlmap(url, param))
    stats[13] = "Done"
    pause()


def step_xss(engine, stats):
    url = input("Enter URL for XSS testing: ").strip()
    param = input(" Parameter to test (e.g. q) [optional]: ").strip() or None
    print(f"→ Running XSS scan on {url} (param={param}) …\n")
    print(engine.run_xss(url, param))
    stats[14] = "Done"
    pause()


def step_report(engine, stats):
    path = input(
        "Enter report filename [report.txt]: ").strip() or "report.txt"
    engine.write_report(path)
    print(f"✓ Report saved to {path}")
    stats[15] = "Done"
    pause()


ACTIONS = {
    "1":  step_target,   "2":  step_info,     "3":  step_scan,
    "4":  step_service,  "5":  step_vuln,     "6":  step_exploit,
    "7":  step_webapp,   "8":  step_bruteforce, "9":  step_postex,
    "10": step_privesc,  "11": step_wireless, "12": step_apicloud,
    "13": step_remed,    "14": step_sqlmap,   "15": step_xss,
    "16": step_report
}


def main():
    # show welcome only once
    show_welcome()

    engine = Engine()
    statuses = ["Pending"] * len(STEPS)

    while True:
        print_ui(statuses)
        choice = input("Select an option: ").strip()
        if choice == "0":
            print("Goodbye!")
            break
        action = ACTIONS.get(choice)
        if action:
            action(engine, statuses)
        else:
            print("Invalid choice.")
            pause()


if __name__ == "__main__":
    main()

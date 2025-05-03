from core.engine import Engine
import os
import sys
import socket
import subprocess
from urllib.parse import urlparse

sys.path.insert(0, os.path.dirname(__file__))

# ─────────────────────────────────────────────────────────────────────────────
BANNER = r"""
██     ██ ██ ██      ██      ███████ ██   ██ ████████ 
██     ██ ██ ██      ██      ██      ██   ██ ██        
██  █  ██ ██ ██      ██      █████   ███████ █████ 
██ ███ ██ ██ ██      ██      ██           ██ ██     
 ███ ███  ██ ███████ ███████ ███████ ███████ ████████
                  Interactive Penetration Testing Framework
"""

WARNING = (
    "WARNING: Educational use only. Obtain authorization before testing any system.\n"
    "Unauthorized testing is illegal."
)

WORKFLOW_STEPS = [
    "Target Setup",  # 1
    "Information Gathering",  # 2
    "Port & Service Scanning",  # 3
    "Exploitation",  # 4
    "Web App Testing",  # 5
    "Brute-Force & Credentials",  # 6
    "Post-Exploitation",  # 7
    "Privilege Escalation",  # 8
    "Wireless & MITM",  # 9
    "Reporting"  # 10
]

RESOURCE_STEPS = [
    "SearchSploit Lookup",  # 11
    "SQL Injection Testing",  # 12
    "XSS Testing"  # 13
    "Pentest Commands"  # 14
]
# ─────────────────────────────────────────────────────────────────────────────


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


def show_welcome():
    clear_screen()
    print("Welcome to WillEye!\n")
    print("An interactive penetration-testing framework — walk through each phase")
    print("from reconnaissance to reporting in a single CLI.\n")

    # ───────────── System-wide tools (APT / Pacman / etc.) ─────────────
    system_tools = [
        "whois", "dig (dnsutils)", "subfinder",
        "nmap", "metasploit-framework (msfconsole)",
        "searchsploit / exploitdb",
        "zap-baseline.py  (from OWASP ZAP)",
        "gobuster", "hydra  +  sshpass",
        "linpeas.sh", "airodump-ng", "bettercap",
        "ffuf", "docker.io"
    ]

    # ───────────── Python packages (install *inside* venv) ─────────────
    venv_packages = [
        "python-nmap", "requests", "paramiko",
        "pywinrm", "colorama", "tabulate"
    ]

    print("Install these **system tools** (outside the venv):")
    for tool in system_tools:
        print(f"  • {tool}")

    print("\nInstall these **Python packages** *inside* your venv:")
    for pkg in venv_packages:
        print(f"  • {pkg}")

    # ───────────── Example one-liner commands ─────────────
    print("\nQuick-install snippets:")
    print("# Outside the venv")
    print("sudo apt update && \\")
    print("sudo apt install -y whois dnsutils subfinder nmap metasploit-framework \\")
    print("    exploitdb zaproxy gobuster hydra sshpass bettercap aircrack-ng ffuf docker.io")
    print("\n# Inside an activated venv")
    print("pip install python-nmap requests paramiko pywinrm colorama tabulate")

    input("\nPress Enter to continue…")


def print_ui(statuses):
    clear_screen()
    print(BANNER)
    print(WARNING + "\n")

    print(f"{' PenTest Workflow ':─^75}")
    print(f"| {'Step':<30} | {'Status':<12} |")
    print(f"{'-'*3}+{'-'*32}+{'-'*14}")
    for idx, step in enumerate(WORKFLOW_STEPS):
        print(f"| {step:<30} | {statuses[idx]:<12} |")
    print(f"{'-'*3}+{'-'*32}+{'-'*14}\n")

    for i, step in enumerate(WORKFLOW_STEPS, 1):
        print(f"  {i}. {step}")

    print(f"\n{' Resources ':─^75}")
    offset = len(WORKFLOW_STEPS)
    for j, step in enumerate(RESOURCE_STEPS, 1):
        print(f"  {offset + j}. {step}")

    print("\n  0. Exit\n")


def pause():
    input("Press Enter to continue...")

# ─────────────────────────────────────────────────────────────────────────────


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
    try:
        print("→ WHOIS lookup:")
        print(engine.run_whois())
    except Exception as e:
        print(f"✗ WHOIS error: {e}")
    try:
        print("\n→ DNS enumeration:")
        print(engine.run_dns_enum())
    except Exception as e:
        print(f"✗ DNS error: {e}")
    try:
        print("\n→ Subdomain discovery:")
        print(engine.run_subdomains())
    except Exception as e:
        print(f"✗ Subdomain error: {e}")
    stats[1] = "Done"
    pause()


def step_scan(engine, stats):
    if not engine.target:
        print("⚠️  Set a target first (step 1).")
        pause()
        return
    print("1) Quick SYN scan (-sS)\n2) Full scan (-sS -sV -sC)")
    choice = input("Select [1-2, default 2]: ").strip() or "2"
    flags = "-sS" if choice == "1" else "-sS -sV -sC"
    ports = input("Enter port range [1-1024]: ").strip() or "1-1024"
    print(f"\n→ Running: nmap {flags} -p {ports} {engine.target}\n")
    try:
        print(engine.run_nmap(flags, ports))
    except Exception as e:
        print(f"✗ Nmap error: {e}")
    stats[2] = "Done"
    pause()


def step_exploit(engine, stats):
    if not engine.target:
        print("⚠️  Set a target first (step 1).")
        pause()
        return
    term = input("Search Metasploit modules (e.g. smb, http): ").strip()
    print(f"\n→ Searching modules for '{term}'…\n")
    try:
        raw = subprocess.check_output(
            ["msfconsole", "-q", "-x", f"search {term}; exit"],
            text=True, stderr=subprocess.DEVNULL
        )
    except FileNotFoundError:
        print("✗ msfconsole not found; install Metasploit.")
        pause()
        return
    except subprocess.CalledProcessError as e:
        raw = e.output
    modules = [l.split()[0]
               for l in raw.splitlines() if l.startswith("exploit/")]
    modules = list(dict.fromkeys(modules))
    if not modules:
        print("No modules found.")
        pause()
        return
    print("Select a module:")
    for i, m in enumerate(modules[:10], 1):
        print(f"  {i}. {m}")
    try:
        sel = int(input(f"Choose [1-{min(10, len(modules))}]: ").strip()) - 1
        module = modules[sel]
    except:
        print("Invalid choice.")
        pause()
        return
    print(f"\n→ Running exploit {module}:\n")
    try:
        print(engine.run_exploit(module))
    except Exception as e:
        print(f"✗ Exploitation error: {e}")
    stats[3] = "Done"
    pause()


def step_webapp(engine, stats):
    print("→ Web App Testing (ZAP + Gobuster):")
    try:
        print(engine.run_webapp_tests())
        stats[4] = "Done"
    except Exception as e:
        print(f"✗ WebApp error: {e}")
    pause()


def step_bruteforce(engine, stats):
    user = input("SSH username: ").strip()
    pwf = input("Password list path: ").strip()
    print(f"→ SSH brute-force as {user}:")
    try:
        print(engine.run_bruteforce(user, pwf))
        stats[5] = "Done"
    except Exception as e:
        print(f"✗ Brute-force error: {e}")
    pause()


def step_postex(engine, stats):
    print("→ Post-Exploitation Enumeration:")
    try:
        print(engine.run_post_exploit())
        stats[6] = "Done"
    except Exception as e:
        print(f"✗ Post-exploit error: {e}")
    pause()


def step_privesc(engine, stats):
    if not engine.target:
        print("⚠️  Set a target first (step 1).")
        pause()
        return
    print("→ Privilege Escalation (linPEAS remote)\n")
    print("1) SSH\n2) Telnet\n3) WinRM")
    m = input("Choose [1-3, default 1]: ").strip() or "1"
    method = {'1': 'ssh', '2': 'telnet', '3': 'winrm'}.get(m, 'ssh')
    user = input("Username: ").strip()
    keyfile = None
    password = None
    port = None
    if method == 'ssh':
        keyfile = input("SSH key file (blank for password): ").strip() or None
        if not keyfile:
            password = input("SSH password: ")
    elif method == 'telnet':
        port = int(input("Telnet port [23]: ").strip() or 23)
        password = input("Telnet password: ")
    else:
        port = int(input("WinRM port [5985]: ").strip() or 5985)
        password = input("WinRM password: ")
    print(f"\n→ Running linPEAS via {method.upper()} …\n")
    try:
        out = engine.run_priv_esc(
            user=user, method=method,
            keyfile=keyfile, password=password,
            port=port
        )
        print(out)
        stats[7] = "Done"
    except Exception as e:
        print(f"✗ PrivEsc error: {e}")
    pause()
# ─────────────────────────────────────────────────────────────────────────────
#  Resource handler: Pentest Commands cheat-sheet


def step_commands(engine, _):
    CHEATSHEET = {
        "Reconnaissance": [
            "whois <domain>",
            "dig <domain> ANY +nocmd +answer",
            "subfinder -d <domain> -o subs.txt"
        ],
        "Port Scanning": [
            "nmap -sS -p- -T4 <target>",
            "nmap -sC -sV -oA nmap/full <target>"
        ],
        "Service Enumeration": [
            "enum4linux -a <target>            # SMB",
            "smtp-user-enum -M VRFY -U users.txt -t <target>",
            "ike-scan -M <target>"
        ],
        "Web Application": [
            "gobuster dir -u https://<host>/ -w common.txt -t 50",
            "nikto -host https://<host>/",
            "zap-baseline.py -t https://<host>/ -r zap.html"
        ],
        "Vulnerability Search": [
            "searchsploit <software version>",
            "nuclei -u https://<host>/ -t cves/"
        ],
        "Exploitation": [
            "msfconsole -q -x 'use exploit/windows/smb/ms17_010_eternalblue; set RHOSTS <target>; run'",
            "sqlmap -u 'https://<host>/item.php?id=1' --dbs"
        ],
        "Post-Exploitation": [
            "linpeas.sh                                  # Linux",
            "winPEAS.exe                                 # Windows",
            "bloodhound-python -c All -u <user>@<dc>"
        ]
    }

    print("\n====================  Pentest Commands Cheat-Sheet  ====================\n")
    for category, cmds in CHEATSHEET.items():
        print(f"[{category}]")
        for cmd in cmds:
            print(f"  {cmd}")
        print()  # blank line between categories
    pause()
# ─────────────────────────────────────────────────────────────────────────────


def step_wireless(engine, stats):
    if not engine.target:
        print("⚠️  Set a target first (step 1).")
        pause()
        return
    print("→ Wireless & MITM via Bettercap:")
    iface = input("Interface [wlan0]: ").strip() or "wlan0"
    gateway = input("Gateway IP (router): ").strip()
    dur = input("Sniff duration in seconds [30]: ").strip() or "30"
    try:
        duration = int(dur)
    except:
        duration = 30
    print(f"\n→ Performing MITM on {engine.target} via {gateway} …\n")
    try:
        print(engine.run_wireless(gateway=gateway, iface=iface, duration=duration))
        stats[8] = "Done"
    except Exception as e:
        print(f"✗ Wireless error: {e}")
    pause()


def step_report(engine, stats):
    path = input("Report filename [report.txt]: ").strip() or "report.txt"
    try:
        engine.write_report(path)
        print(f"✓ Report saved to {path}")
        stats[9] = "Done"
    except Exception as e:
        print(f"✗ Reporting error: {e}")
    pause()

# ─────────────────────────────────────────────────────────────────────────────


def step_searchsploit(engine, _):
    term = input("SearchSploit term: ").strip()
    try:
        print(f"→ SearchSploit for '{term}':")
        print(engine.run_searchsploit(term))
    except Exception as e:
        print(f"✗ SearchSploit error: {e}")
    pause()


def step_sqlmap(engine, _):
    url = input("Enter URL for SQLi testing: ").strip()
    param = input("Parameter (e.g. id) [optional]: ").strip() or None
    print(f"→ sqlmap on {url} (param={param}):")
    try:
        print(engine.run_sqlmap(url, param))
    except Exception as e:
        print(f"✗ SQLi error: {e}")
    pause()


def step_xss(engine, _):
    url = input("Enter URL for XSS testing: ").strip()
    param = input("Parameter (e.g. q) [optional]: ").strip() or None
    print(f"→ XSS scan on {url} (param={param}):")
    try:
        print(engine.run_xss(url, param))
    except Exception as e:
        print(f"✗ XSS error: {e}")
    pause()


# ─────────────────────────────────────────────────────────────────────────────
ACTIONS = {
    "1":  step_target,
    "2":  step_info,
    "3":  step_scan,
    "4":  step_exploit,
    "5":  step_webapp,
    "6":  step_bruteforce,
    "7":  step_postex,
    "8":  step_privesc,
    "9":  step_wireless,
    "10": step_report,
    "11": step_searchsploit,
    "12": step_sqlmap,
    "13": step_xss,
    "14": step_commands,
}


def main():
    show_welcome()
    engine = Engine()
    statuses = ["Pending"] * len(WORKFLOW_STEPS)

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

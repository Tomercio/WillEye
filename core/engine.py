# core/engine.py
import socket

from core.adapters import (
    whois_adapter,
    dns_adapter,
    nmap_adapter,
    searchsploit_adapter,
    metasploit_adapter,
    zap_baseline,
    dir_bruteforce,
    ssh_bruteforce,
    notionally_post_exploit,
    run_linpeas,
    wireless_tests,
    api_fuzz,
    remediation_guide,
)


class Engine:
    def __init__(self):
        self.target = None
        self.history = {}

    def _ensure_target(self):
        if not self.target:
            raise RuntimeError("Target not set. Complete step 1 first.")

    def run_whois(self):
        self._ensure_target()
        out = whois_adapter.lookup(self.target)
        self.history['whois'] = out
        return out

    def run_dns_enum(self):
        self._ensure_target()
        out = dns_adapter.dig(self.target)
        self.history['dns'] = out
        return out

    def run_subdomains(self):
        self._ensure_target()
        out = dns_adapter.subdomains(self.target)
        self.history['subdomains'] = out
        return out

    def run_nmap(self, flags: str, ports: str):
        self._ensure_target()
        out = nmap_adapter.scan(self.target, flags, ports)
        self.history['nmap'] = out
        return out

    def run_service_enum(self):
        self._ensure_target()
        flags = "-sV -sC"
        ports = "1-65535"
        out = nmap_adapter.scan(self.target, flags, ports)
        self.history['service_enum'] = out
        return out

    def run_searchsploit(self, term: str):
        out = searchsploit_adapter.search(term)
        self.history.setdefault('vuln', "")
        self.history['vuln'] += out + "\n"
        return out

    def run_exploit(self, module: str):
        self._ensure_target()
        out = metasploit_adapter.exploit(self.target, module)
        self.history['exploit'] = out
        return out

    def run_webapp_tests(self):
        self._ensure_target()
        o1 = zap_baseline(self.target)
        o2 = dir_bruteforce(self.target)
        combined = f"--- ZAP Baseline ---\n{o1}\n--- Dir Bruteforce ---\n{o2}"
        self.history['webapp'] = combined
        return combined

    def run_bruteforce(self, user: str, pwlist: str):
        self._ensure_target()
        out = ssh_bruteforce(self.target, user, pwlist)
        self.history['bruteforce'] = out
        return out

    def run_post_exploit(self):
        self._ensure_target()
        out = notionally_post_exploit(self.target)
        self.history['post_exploit'] = out
        return out

    def run_priv_esc(self):
        self._ensure_target()
        out = run_linpeas()
        self.history['priv_esc'] = out
        return out

    def run_wireless(self):
        out = wireless_tests()
        self.history['wireless'] = out
        return out

    def run_api_cloud(self):
        self._ensure_target()
        out = api_fuzz(self.target)
        self.history['api_cloud'] = out
        return out

    def run_remediation(self):
        out = remediation_guide(self.history)
        self.history['remediation'] = out
        return out

    def write_report(self, filename: str):
        with open(filename, 'w') as f:
            for phase, out in self.history.items():
                f.write(f"=== {phase.upper()} ===\n{out}\n\n")

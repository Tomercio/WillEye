# core/engine.py

import socket

from core.adapters import (
    whois_adapter,
    dns_adapter,
    nmap_adapter,
    searchsploit_adapter,
)


class Engine:
    def __init__(self):
        self.target = None
        self.history = {}

    def _ensure_target(self):
        if not self.target:
            raise RuntimeError(
                "Target not set. Run: pentest target set <host>")

    def run_whois(self):
        self._ensure_target()
        res = whois_adapter.lookup(self.target)
        self.history['whois'] = res
        return res

    def run_dns_enum(self):
        self._ensure_target()
        res = dns_adapter.dig(self.target)
        self.history['dns'] = res
        return res

    def run_subdomains(self):
        self._ensure_target()
        res = dns_adapter.subdomains(self.target)
        self.history['subdomains'] = res
        return res

    def run_nmap(self, scan_type, ports):
        self._ensure_target()
        res = nmap_adapter.scan(self.target, scan_type, ports)
        self.history['nmap'] = res
        return res

    def run_searchsploit(self, term):
        if not term:
            raise RuntimeError("SearchSploit term cannot be empty")
        res = searchsploit_adapter.search(term)
        # accumulate multiple searches
        self.history.setdefault('vuln', '')
        self.history['vuln'] += res + "\n"
        return res

    def write_report(self, filename):
        with open(filename, 'w') as f:
            for phase, out in self.history.items():
                f.write(f"=== {phase.upper()} ===\n{out}\n\n")

import socket

from core.adapters import (
    whois_adapter,
    dig,
    subdomains,
    nmap_adapter,
    searchsploit_adapter,
    metasploit_adapter,
    zap_baseline,
    dir_bruteforce,
    ssh_bruteforce,
    notionally_post_exploit,
    run_linpeas,
    wireless_tests,
    sqlmap_scan,
    xss_scan,
)


class Engine:
    def __init__(self):
        self.target = None
        self.history = {}

    def _ensure_target(self):
        if not self.target:
            raise RuntimeError("Target not set. Complete step 1 first.")

    def run_whois(self) -> str:
        self._ensure_target()
        out = whois_adapter(self.target)
        self.history['whois'] = out
        return out

    def run_dns_enum(self) -> str:
        self._ensure_target()
        out = dig(self.target)
        self.history['dns'] = out
        return out

    def run_subdomains(self) -> str:
        self._ensure_target()
        out = subdomains(self.target)
        self.history['subdomains'] = out
        return out

    def run_nmap(self, flags: str, ports: str) -> str:
        self._ensure_target()
        out = nmap_adapter(self.target, flags, ports)
        self.history['nmap'] = out
        return out

    def run_searchsploit(self, term: str) -> str:
        out = searchsploit_adapter(term)
        self.history.setdefault('vuln', "")
        self.history['vuln'] += out + "\n"
        return out

    def run_exploit(self, module: str) -> str:
        self._ensure_target()
        out = metasploit_adapter(self.target, module)
        self.history['exploit'] = out
        return out

    def run_webapp_tests(self) -> str:
        self._ensure_target()
        o1 = zap_baseline(self.target)
        o2 = dir_bruteforce(self.target)
        combined = f"--- ZAP Baseline ---\n{o1}\n--- Dir Bruteforce ---\n{o2}"
        self.history['webapp'] = combined
        return combined

    def run_bruteforce(self, user: str, pwlist: str) -> str:
        self._ensure_target()
        out = ssh_bruteforce(self.target, user, pwlist)
        self.history['bruteforce'] = out
        return out

    def run_post_exploit(self) -> str:
        self._ensure_target()
        out = notionally_post_exploit(self.target)
        self.history['post_exploit'] = out
        return out

    def run_priv_esc(
        self,
        user: str,
        method: str = 'ssh',
        keyfile: str = None,
        password: str = None,
        port: int = None
    ) -> str:
        self._ensure_target()
        out = run_linpeas(
            target=self.target,
            user=user,
            method=method,
            keyfile=keyfile,
            password=password,
            port=port
        )
        self.history['priv_esc'] = out
        return out

    def run_wireless(
        self,
        gateway: str,
        iface: str = "wlan0",
        duration: int = 30
    ) -> str:
        """
        Perform MITM against self.target via the given gateway/interface for duration seconds.
        """
        self._ensure_target()
        out = wireless_tests(self.target, gateway, iface, duration)
        self.history['wireless'] = out
        return out

    def run_sqlmap(
        self,
        url: str,
        param: str = None,
        level: int = 1,
        risk: int = 1
    ) -> str:
        self._ensure_target()
        out = sqlmap_scan(url, param, level, risk)
        self.history['sqlmap'] = out
        return out

    def run_xss(self, url: str, param: str = None) -> str:
        self._ensure_target()
        out = xss_scan(url, param)
        self.history['xss'] = out
        return out

    def write_report(self, filename: str):
        with open(filename, 'w') as f:
            for phase, out in self.history.items():
                f.write(f"=== {phase.upper()} ===\n{out}\n\n")

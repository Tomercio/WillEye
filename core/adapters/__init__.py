# core/adapters/__init__.py

from .whois_adapter import lookup as whois_adapter
from .dns_adapter import dig, subdomains
from .nmap_adapter import scan as nmap_adapter
from .searchsploit_adapter import search as searchsploit_adapter
from .metasploit_adapter import exploit as metasploit_adapter
from .webapp_adapter import zap_baseline, dir_bruteforce
from .bruteforce_adapter import ssh_bruteforce
from .post_exploit_adapter import notionally_post_exploit
from .priv_esc_adapter import run_linpeas
from .wireless_adapter import wireless_tests
from .sqlmap_adapter import sqlmap_scan
from .xss_adapter import xss_scan

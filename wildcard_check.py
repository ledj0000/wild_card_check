#!/usr/bin/env python3
"""
Wildcard DNS Detector
Author: ledj.org rebel edition
Usage: python wildcard_check.py example.com
"""

import sys
import random
import string
import dns.resolver

def random_subdomain(length=12):
    """Generate a random subdomain string."""
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))

def resolve_domain(domain):
    """Try to resolve a domain, return list of IPs or empty list."""
    try:
        answers = dns.resolver.resolve(domain, 'A')
        return [answer.to_text() for answer in answers]
    except Exception:
        return []

def check_wildcard(domain):
    """Check if a domain uses wildcard DNS."""
    # Resolve base domain first
    base_ips = resolve_domain(domain)
    if not base_ips:
        print(f"[!] Could not resolve {domain}")
        return False

    print(f"[+] {domain} resolves to: {base_ips}")

    # Generate random subdomain
    sub = f"{random_subdomain()}.{domain}"
    sub_ips = resolve_domain(sub)

    if sub_ips:
        print(f"[+] {sub} unexpectedly resolves to: {sub_ips}")
        if set(sub_ips) == set(base_ips):
            print("[*] This looks like a classic wildcard DNS setup.")
        else:
            print("[*] This domain resolves differently, may use partial wildcard.")
        return True
    else:
        print(f"[-] {sub} did not resolve. Likely no wildcard DNS.")
        return False

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python wildcard_check.py <domain>")
        sys.exit(1)

    domain = sys.argv[1].strip()
    print(f"[*] Testing {domain} for wildcard DNS...")
    result = check_wildcard(domain)

    if result:
        print("[+] Wildcard DNS detected.")
    else:
        print("[-] No wildcard DNS detected.")

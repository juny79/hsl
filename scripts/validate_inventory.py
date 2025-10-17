#!/usr/bin/env python3
"""Validate inventory files (assets.yaml, ipam.csv) for basic sanity checks."""
import yaml, csv, sys, ipaddress, pathlib

def load_yaml(p): return yaml.safe_load(pathlib.Path(p).read_text(encoding='utf-8'))
def load_csv(p):
    rows = []
    with open(p, newline='', encoding='utf-8') as f:
        for r in csv.DictReader(f):
            rows.append(r)
    return rows

def main():
    base = pathlib.Path(__file__).resolve().parents[1] / 'inventory'
    assets = load_yaml(base / 'assets.yaml')
    ipam = load_csv(base / 'ipam.csv')

    errors = []
    # Check IP format
    for row in ipam:
        ip = row.get('ip','')
        if 'X' in ip:
            errors.append(f"IP not finalized: {row.get('hostname')} -> {ip}")
            continue
        try:
            ipaddress.ip_address(ip)
        except Exception:
            errors.append(f"Invalid IP: {row.get('hostname')} -> {ip}")

    # Check duplicates
    ips = [r['ip'] for r in ipam if 'X' not in r['ip']]
    dups = set([x for x in ips if ips.count(x) > 1])
    if dups:
        errors.append(f"Duplicate IP(s): {', '.join(sorted(dups))}")

    # Ensure asset hostnames exist in ipam
    asset_hosts = {s['name'] for s in assets.get('servers',[])}
    ipam_hosts = {r['hostname'] for r in ipam}
    missing = asset_hosts - ipam_hosts
    if missing:
        errors.append(f"Missing in ipam.csv: {', '.join(sorted(missing))}")

    if errors:
        print("VALIDATION FAILED:\n - " + "\n - ".join(errors))
        sys.exit(1)
    else:
        print("OK: inventory files look sane.")

if __name__ == '__main__':
    main()
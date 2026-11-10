#!/usr/bin/env python3
"""TwinNet | Local logic simulation of AWS VPC peering.

No AWS resources are created and no real packets are sent. Route tables and
security-group inbound rules are plain dictionaries; each simulated packet is
checked for (1) a matching route and (2) a destination inbound rule.
Standard library only.
"""
import ipaddress
from copy import deepcopy

PEER = "pcx-ewb-a-b-peer"

HOSTS = {
    "bastion": {"ip": "10.10.1.10", "rt": "A-public", "sg": "ewb-sg-bastion"},
    "app-a": {"ip": "10.10.2.10", "rt": "A-private", "sg": "ewb-sg-app-a"},
    "app-b": {"ip": "10.20.1.10", "rt": "B-private", "sg": "ewb-sg-app-b"},
}

# Baseline: local routes only (no peering routes yet)
ROUTES_BASELINE = {
    "A-public": [("10.10.0.0/16", "local"), ("0.0.0.0/0", "igw")],
    "A-private": [("10.10.0.0/16", "local")],
    "B-private": [("10.20.0.0/16", "local")],
}

PEERING_ROUTES = {
    "A-public": ("10.20.0.0/16", PEER),
    "A-private": ("10.20.0.0/16", PEER),
    "B-private": ("10.10.0.0/16", PEER),
}

SG_RULES = {
    "ewb-sg-app-a": [("10.10.1.10/32", "tcp", 22), ("10.20.1.10/32", "icmp", None)],
    "ewb-sg-app-b": [("10.10.1.10/32", "tcp", 22), ("10.10.2.10/32", "icmp", None)],
}


def best_route(routes, dst):
    """Longest-prefix match, as a VPC route table does."""
    dst = ipaddress.ip_address(dst)
    hits = [(ipaddress.ip_network(c), t) for c, t in routes if dst in ipaddress.ip_network(c)]
    return max(hits, key=lambda h: h[0].prefixlen) if hits else None


def sg_allows(sg, src, proto, port):
    src = ipaddress.ip_address(src)
    for cidr, p, prt in SG_RULES.get(sg, []):
        if src in ipaddress.ip_network(cidr) and p == proto and (prt is None or prt == port):
            return True
    return False


def check(routes, src, dst, proto="icmp", port=None):
    s, d = HOSTS[src], HOSTS[dst]
    hit = best_route(routes[s["rt"]], d["ip"])
    route_ok = bool(hit) and hit[1] == PEER
    sg_ok = sg_allows(d["sg"], s["ip"], proto, port)
    return {
        "src": src, "dst": dst, "packet": f"{s['ip']} -> {d['ip']} ({proto.upper()})",
        "route": f"{s['rt']}: {hit[0]} -> {hit[1]}" if hit else "No matching route",
        "route_ok": route_ok, "sg": "ALLOW" if sg_ok else "DENY",
        "result": "PASS" if route_ok and sg_ok else "BLOCKED",
    }


def show(title, r):
    print(f"{title}: {r['result']}")
    print(f"  Packet: {r['packet']}")
    print(f"  Route: {r['route']}")
    print(f"  Destination inbound rule: {r['sg']}")


def main():
    bar = "=" * 62
    print(bar)
    print("TWINNET | AWS VPC PEERING - LOCAL LOGIC SIMULATION")
    print("No AWS resources are created; no real packets are transmitted.")
    print(bar)

    print("1) BASELINE BEFORE PEERING")
    base = check(ROUTES_BASELINE, "app-a", "app-b")
    show("App-A to App-B before peering", base)

    routes = deepcopy(ROUTES_BASELINE)
    for table, entry in PEERING_ROUTES.items():
        routes[table].append(entry)

    print("2) CONNECTIVITY AFTER PEERING ROUTES")
    fwd = check(routes, "app-a", "app-b")
    rev = check(routes, "app-b", "app-a")
    show("Forward: App-A to App-B", fwd)
    show("Reverse: App-B to App-A", rev)

    print("3) CONTROLLED SECURITY-GROUP FAILURE")
    removed = ("10.10.2.10/32", "icmp", None)
    SG_RULES["ewb-sg-app-b"].remove(("10.10.2.10/32", "icmp", None))
    fail = check(routes, "app-a", "app-b")
    show("App-A to App-B after removing ICMP rule", fail)

    print("4) RECOVERY AFTER RESTORING ICMP RULE")
    SG_RULES["ewb-sg-app-b"].append(removed)
    rec = check(routes, "app-a", "app-b")
    show("App-A to App-B after restoring ICMP rule", rec)

    print("5) PRIVATE-HOST ADDRESS CHECK")
    for h in ("app-a", "app-b"):
        print(f"  {h.title().replace('-', '-')} private address: {HOSTS[h]['ip']} | Public IP: NONE (design)")

    print("SIMULATION SUMMARY")
    print(f"  Baseline blocked: {'YES (expected)' if base['result'] == 'BLOCKED' else 'NO'}")
    print(f"  Forward and reverse logical checks passed: {fwd['result'] == rev['result'] == 'PASS'}")
    print(f"  Removing inbound ICMP blocked traffic: {fail['result'] == 'BLOCKED'}")
    print(f"  Restoring inbound ICMP restored traffic: {rec['result'] == 'PASS'}")
    print("Note: These are deterministic configuration checks, not AWS or OS-level ping results.")


if __name__ == "__main__":
    main()

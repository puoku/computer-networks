import csv
import ipaddress
import socket
import subprocess
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
DOMAINS_FILE = BASE_DIR / "domains.txt"
RESULTS_FILE = BASE_DIR / "results.csv"


def get_domains():
    return [
        line.strip()
        for line in DOMAINS_FILE.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


def resolve_domain(domain):
    ips = set()
    for item in socket.getaddrinfo(domain, None):
        ips.add(item[4][0])
    return sorted(ips)


def traceroute_ip(ip):
    is_ipv6 = ipaddress.ip_address(ip).version == 6
    command = ["traceroute", "-m", "5", "-w", "1"]
    if is_ipv6:
        command.append("-6")
    command.append(ip)

    result = subprocess.run(
        command,
        capture_output=True,
        text=True,
        check=False,
    )
    return result.stdout


def parse_traceroute(output):
    rows = []
    for line in output.splitlines():
        line = line.strip()
        if not line or line.lower().startswith("traceroute"):
            continue

        parts = line.split()
        if not parts or not parts[0].isdigit():
            continue

        hop = parts[0]
        hop_ip = "*"

        for part in parts[1:]:
            candidate = part.strip("()")
            try:
                ipaddress.ip_address(candidate)
                hop_ip = candidate
                break
            except ValueError:
                continue

        rows.append((hop, hop_ip, line))

    return rows


def main():
    domains = get_domains()

    with RESULTS_FILE.open("w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["domain", "ip", "hop", "hop_ip", "raw_line"])

        for domain in domains:
            ips = resolve_domain(domain)

            for ip in ips:
                output = traceroute_ip(ip)
                hops = parse_traceroute(output)

                if not hops:
                    writer.writerow([domain, ip, "", "", "traceroute failed or no hops"])
                    continue

                for hop, hop_ip, raw_line in hops:
                    writer.writerow([domain, ip, hop, hop_ip, raw_line])

    print(f"Saved results to {RESULTS_FILE}")


if __name__ == "__main__":
    main()

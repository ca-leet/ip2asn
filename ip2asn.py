import ipinfo
import argparse
import os
import time
import csv
import re
from datetime import datetime
from requests.exceptions import RequestException

parser = argparse.ArgumentParser(
    description="Bulk IP Address to ASN lookup (CSV + TXT output)"
)

parser.add_argument("-l", "--list", help="Line-separated list of IPs")
parser.add_argument("-o", "--output", required=True, help="Base output name (no extension)")
parser.add_argument("--party", default="Third-Party")
parser.add_argument("--in-scope", default="")
parser.add_argument("--notes", default="")
parser.add_argument("--source", default="ipinfo")

args = parser.parse_args()

access_token = os.getenv("IPINFO_API_KEY") or input("Enter IPInfo API key: ")
handler = ipinfo.getHandler(access_token)

CSV_HEADERS = [
    "ASN",
    "IP Address",
    "Owner",
    "Client/Third-Party",
    "In Scope?",
    "Notes",
    "Discovered Date",
    "Source",
]

ASN_RE = re.compile(r"\bAS\d+\b")

def parse_asn_and_owner(details):
    org = getattr(details, "org", "") or ""
    asn = ""

    m = ASN_RE.search(org)
    if m:
        asn = m.group(0)

    owner = ASN_RE.sub("", org, count=1).strip(" -–—")
    return asn, owner

def lookup_ip(ip):
    details = handler.getDetails(ip)
    asn, owner = parse_asn_and_owner(details)
    date = datetime.now().strftime("%-m/%-d/%y")

    return {
        "ASN": asn,
        "IP Address": ip,
        "Owner": owner,
        "Client/Third-Party": args.party,
        "In Scope?": args.in_scope,
        "Notes": args.notes,
        "Discovered Date": date,
        "Source": args.source,
    }

def write_csv(path, row):
    exists = os.path.exists(path)
    with open(path, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=CSV_HEADERS)
        if not exists:
            writer.writeheader()
        writer.writerow(row)

def write_txt(path, row):
    with open(path, "a", encoding="utf-8") as f:
        for k, v in row.items():
            f.write(f"{k:<18}: {v}\n")
        f.write("-" * 50 + "\n")

def main():
    csv_file = f"{args.output}.csv"
    txt_file = f"{args.output}.txt"

    ips = []
    if args.list:
        with open(args.list) as f:
            ips = [line.strip() for line in f if line.strip()]
    else:
        ips = [input("Enter IP address: ").strip()]

    for ip in ips:
        try:
            row = lookup_ip(ip)
        except RequestException as e:
            row = {
                "ASN": "",
                "IP Address": ip,
                "Owner": f"ERROR: {e}",
                "Client/Third-Party": args.party,
                "In Scope?": args.in_scope,
                "Notes": args.notes,
                "Discovered Date": datetime.now().strftime("%-m/%-d/%y"),
                "Source": args.source,
            }

        write_csv(csv_file, row)
        write_txt(txt_file, row)
        time.sleep(0.1)

if __name__ == "__main__":
    main()

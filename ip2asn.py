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

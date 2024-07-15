import ipinfo
import argparse
import os
import time
from requests.exceptions import RequestException

parser = argparse.ArgumentParser(
    description="Bulk IP Address to ASN lookup",
    epilog="Set your IPInfo API key as an environment variable: export IPINFO_API_KEY=your_api_key",
    formatter_class=argparse.RawDescriptionHelpFormatter
)

parser.add_argument("-l", "--list", type=str, help="Path to line-separated list of IP addresses to lookup")
parser.add_argument("-o", "--output", type=str, help="Name of output file (txt)")

args = parser.parse_args()

access_token = os.getenv('IPINFO_API_KEY')
if not access_token:
    access_token = input("Enter your IPInfo API key: ")

handler = ipinfo.getHandler(access_token)

# get and store asn details function in details dict
def get_asn_details(ip_address):
    try:
        details = handler.getDetails(ip_address)
        return {
            "ip address: ": ip_address,
            "city: ": details.city,
            "region: ": details.region,
            "organization: ": details.org,
        }
    except RequestException as e:
        return {"ip address ": ip_address, "error": str(e)}

# print asn details function using details dict
def print_asn_details(details, output_file=None):
    output = ""
    if isinstance(details, dict):
        for key, value in details.items():
            line = f"{key.capitalize()}: {value}\n"
            output += line
            print(line, end='')
    else:
        error_message = f"Error: Unbale to Process Data for: {details}"
        output += error_message
        print(error_message, end='')

    output += '\n'
    print()

    if output_file:
        with open(output_file, 'a') as file:
            file.write(output)

# run ip addresses through get/print_asn_details functions or take input if no list provided
def main():
    output_file = args.output
    if args.list:
        with open(args.list, 'r') as file:
            ip_addresses = file.read().splitlines()
        for ip in ip_addresses:
            details = get_asn_details(ip)
            print_asn_details(details, output_file)
            time.sleep(.1)
    else:
        ip_address = input("Enter the ip address to lookup: ")
        details = get_asn_details(ip_address)
        print_asn_details(details, output_file)

if __name__ == "__main__":
    main()

import dns.resolver

def get_sorted_mx_ips(domain):
    """
    Queries DNS MX records for the specified domain, sorts them by priority preference, and resolves each exchange server host to its IPv4 address.
    """
    try:
        # 1. Query the MX records for the given domain
        mx_records = dns.resolver.resolve(domain, 'MX')
        
        # 2. Sort records by their preference value (lower number means higher priority)
        sorted_records = sorted(mx_records, key=lambda record: record.preference)
        
        # 3. Resolve IP address for each mail server
        for record in sorted_records:
            preference = record.preference
            exchange_host = str(record.exchange)
            
            try:
                # Query A record (IPv4) for the target exchange host
                ip_records = dns.resolver.resolve(exchange_host, 'A')
                for ip in ip_records:
                    print(f"{preference}\t{exchange_host}\t{ip}")
            except Exception as e:
                print(f"{preference}\t{exchange_host}\t[Could not resolve IP: {e}]")

    except Exception as e:
        print(f"Error querying MX records for {domain}: {e}")

if __name__ == "__main__":
    target_domain = "gmail.com"
    print(f"MX Records and resolved IPs for @{target_domain} (Sorted by Priority):\n")
    get_sorted_mx_ips(target_domain)
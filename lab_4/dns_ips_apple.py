import dns.resolver

dominio = 'apple.com'

try:
    respuestas = dns.resolver.resolve(dominio, 'A')

    print(f"IP addresses for {dominio}:")
    print("-" * 40)

    for rdata in respuestas:
        print(f"- {rdata.address}")

except Exception as e:
    print(f"Error resolving domain {dominio}: {e}")
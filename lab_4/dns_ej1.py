import dns.resolver

respuesta = dns.resolver.query('en.wikipedia.org')

print("-" * 50)
print(respuesta[0].address)
print("-" * 50)


print(respuesta.response)
print("-" * 50)

print(respuesta.response.to_wire())
print("-" * 50)
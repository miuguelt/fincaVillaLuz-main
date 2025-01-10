import json

# Carga el archivo acme.json
with open('/data/coolify/proxy/acme.json', 'r') as file:
    acme_data = json.load(file)

# Extrae los certificados para el dominio específico
domain = "finca.isladigital.xyz"  # El dominio para el cual quieres extraer el certificado

cert_data = acme_data['Certificates'][0]  # Asegúrate de que 'Certificates' contiene la entrada correcta

cert_pem = cert_data['certificate']
key_pem = cert_data['key']

# Escribe los archivos cert.pem y key.pem
with open('/data/coolify/proxy/cert.pem', 'w') as cert_file:
    cert_file.write(cert_pem)

with open('/data/coolify/proxy/key.pem', 'w') as key_file:
    key_file.write(key_pem)

print("Certificados extraídos correctamente.")

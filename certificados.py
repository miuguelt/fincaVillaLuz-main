import json

def extract_certificates(domain):
    try:
        # Carga el archivo acme.json
        with open('proxy/acme.json', 'r') as file:
            acme_data = json.load(file)

        # Accede a la lista de certificados
        certificates = acme_data['letsencrypt']['Certificates']

        # Busca el certificado para el dominio específico
        for cert in certificates:
            if cert['domain']['main'] == domain:
                cert_pem = cert['certificate']
                key_pem = cert['key']

                # Escribe los archivos cert.pem y key.pem
                with open('proxy/cert.pem', 'w') as cert_file:
                    cert_file.write(cert_pem)

                with open('proxy/key.pem', 'w') as key_file:
                    key_file.write(key_pem)

                print(f"Certificados para {domain} extraídos correctamente.")
                return

        print(f"No se encontró un certificado para el dominio {domain}.")
    except FileNotFoundError:
        print("Error: El archivo proxy/acme.json no se encontró.")
    except KeyError:
        print("Error: La estructura del archivo acme.json no es la esperada.")
    except Exception as e:
        print(f"Error inesperado: {e}")

# Dominio para el cual extraer el certificado
domain = "finca.isladigital.xyz"
# Extrae los certificados
extract_certificates(domain)
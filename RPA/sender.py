import requests
import logs

def enviar_atos(resultado, headers, api_url):
    sucessos = 0
    erros = 0

    for item in resultado:
        try:
            numero_limpo = ''.join(filter(str.isdigit, item["numero_ato"]))
            numero_limpo = int(numero_limpo) if numero_limpo else 0

            payload = {
                "name": "Receita Federal",
                "tipo_ato": item["tipo_ato"],
                "numero_ato": numero_limpo,
                "orgao": item["orgao_unidade"],
                "publicacao": item["publicacao"],
                "ementa": item["ementa"]
            }

            response = requests.post(f"{api_url}/atos", json=payload, headers=headers)

            if response.status_code in [200, 201]:
                sucessos += 1
                logs.log(f"Enviado Ato N: {payload['numero_ato']}")
            else:
                erros += 1
                logs.log(f"Erro ao eviar ato \"{numero_limpo}\" {response.status_code}: {response.text}", type="error")

        except Exception as e:
            erros += 1
            logs.log(f"Erro ao enviar ato: {e}", type="error")

    return sucessos, erros
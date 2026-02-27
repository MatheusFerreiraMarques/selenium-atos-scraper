from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.common.by import By
from datetime import datetime, timedelta
import logs
import time


def coletar_atos(dias_atras=3, max_paginas=10):
    hoje = datetime.now()
    dt_inicio = hoje - timedelta(days=dias_atras)

    dt_inicio_url = dt_inicio.strftime("%d%%2F%m%%2F%Y")
    dt_fim_url = hoje.strftime("%d%%2F%m%%2F%Y")
    ano_atual = hoje.strftime("%Y")

    options = ChromeOptions()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    navegador = Chrome(options=options)

    resultado = []

    for pagina in range(1, max_paginas + 1):
        logs.log(f"Tentando coletar página {pagina}...")

        url = (
            "https://normas.receita.fazenda.gov.br/sijut2consulta/consulta.action"
            f"?tipoData=2"
            f"&dt_inicio={dt_inicio_url}"
            f"&dt_fim={dt_fim_url}"
            f"&ano_ato={ano_atual}"
            f"&optOrdem=Publicacao_DESC"
            f"&p={pagina}"
        )

        navegador.get(url)
        time.sleep(2)

        linhas = navegador.find_elements(By.CSS_SELECTOR, "tr.linhaResultados")

        if not linhas:
            logs.log("Não há mais resultados.")
            break

        for linha in linhas:
            tds = linha.find_elements(By.TAG_NAME, "td")
            if len(tds) >= 5:
                tipo_ato = tds[0].text.strip()
                numero_ato = tds[1].text.strip()
                orgao = tds[2].text.strip()
                publicacao_str = tds[3].text.strip()
                ementa = tds[4].text.strip()

                publicacao_date = datetime.strptime(
                    publicacao_str, "%d/%m/%Y"
                ).date()

                resultado.append({
                    "tipo_ato": tipo_ato,
                    "numero_ato": numero_ato,
                    "orgao_unidade": orgao,
                    "publicacao": publicacao_date.isoformat(),
                    "ementa": ementa
                })

    navegador.quit()
    return resultado
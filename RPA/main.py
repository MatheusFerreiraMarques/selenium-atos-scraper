import os
import time
import requests
import argparse
import schedule
import logs
from dotenv import load_dotenv
from scraper import coletar_atos
from sender import enviar_atos

def run():
    API_URL = os.getenv("API_URL")
    API_USERNAME = os.getenv("API_USERNAME")
    API_PASSWORD = os.getenv("API_PASSWORD")
    start_time = time.time()

    auth_response = requests.post(
        f"{API_URL}/auth/",
        data={"username": API_USERNAME, "password": API_PASSWORD}
    )
    token = auth_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    resultado = coletar_atos(dias_atras=3)
    logs.log(f"Total capturado: {len(resultado)}")

    sucessos, erros = enviar_atos(resultado, headers, api_url=API_URL)

    logs.log(f"Resumo:")
    logs.log(f"Sucessos: {sucessos}")
    logs.log(f"Erros: {erros}")

    tempo_execucao = int(time.time() - start_time)
    logs.log(f"Tempo de execução {tempo_execucao} segundos")

def run_scheduled():
    logs.log("Running task:")
    run()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--schedule", default=0, type=int)

    logs.setup_logs()
    args = parser.parse_args()

    load_dotenv()

    if args.schedule == 0:
        run()
    else:
        logs.log("Running in scheduled mode")
        schedule.every(args.schedule).seconds.do(run_scheduled)
        
        run()
        while True:
            schedule.run_pending()
            time.sleep(15)

if __name__ == "__main__":
    main()
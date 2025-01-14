import time
import json
import os
import pandas as pd
from webDriverConf import configure_driver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

# Config env
config = json.load(open('config.json'))

url_base = config['url_base']
file_path = config['file_path']
sheet = config['sheet']
download_folder = config['download_folder']
element_ids = config['element_ids']

# IDs elementos (HTML)
renavam_input_id = element_ids['renavam_input']
consultar_button_id = element_ids['consultar_button']
download_button_id = element_ids['download_button']

# WebDriver
driver = configure_driver()

# Main
def main():
    try:
        print("[INFO] Lendo a planilha.")
        df = pd.read_excel(file_path, sheet_name=sheet)

        # Validar colunas
        required_columns = ["Renavam", "Placa"]
        if not all(col in df.columns for col in required_columns):
            print("[ERROR] A planilha não contém todas as colunas necessárias.")
            return

        for _, row in df.iterrows():
            renavam = str(row["Renavam"])
            placa = row["Placa"]
            print(f"[INFO] Processando: Renavam={renavam}, Placa={placa}")

            print("[INFO] Acessando Home.")
            driver.get(url_base + "/home")

            try:
                print("[DEBUG] Aguardando o campo Renavam.")
                renavam_input = WebDriverWait(driver, 90).until(
                    EC.presence_of_element_located((By.ID, renavam_input_id))
                )
                renavam_input.clear()
                renavam_input.send_keys(renavam)
                print("[INFO] Renavam preenchido.")
            except TimeoutException:
                print("[ERROR] Não foi possível localizar o campo Renavam.")
                continue

            try:
                print("[DEBUG] Localizando o botão CONSULTAR.")
                consultar_button = WebDriverWait(driver, 90).until(
                    EC.element_to_be_clickable((By.ID, consultar_button_id))
                )
                consultar_button.click()
                print("[INFO] Botão CONSULTAR clicado com sucesso.")
            except TimeoutException:
                print("[ERROR] Não foi possível clicar no botão CONSULTAR.")
                continue

            try:
                print("[DEBUG] Aguardando o botão de download.")
                download_button = WebDriverWait(driver, 90).until(
                    EC.element_to_be_clickable((By.ID, download_button_id))
                )
                download_button.click()
                print("[INFO] Botão de download clicado com sucesso.")
            except TimeoutException:
                print("[ERROR] Não foi possível localizar ou clicar no botão de download.")
                continue

    except Exception as e:
        print(f"[ERROR] Um erro inesperado ocorreu: {e}")
    finally:
        print("[INFO] Finalizando o WebDriver.")
        driver.quit()

if __name__ == "__main__":
    main()
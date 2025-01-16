import time
import json
import os
import pandas as pd
from webDriverConf import configure_driver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException

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

def wait_for_page_load(driver, timeout=30):
    """
    Aguarda até que a página tenha terminado de carregar.
    """
    WebDriverWait(driver, timeout).until(
        lambda d: d.execute_script("return document.readyState") == "complete"
    )

def wait_for_element(driver, by, value, timeout=90):
    """
    Aguarda até que um elemento esteja presente e estável no DOM.
    """
    return WebDriverWait(driver, timeout).until(
        EC.presence_of_element_located((by, value))
    )

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
            wait_for_page_load(driver)

            try:
                print("[DEBUG] Aguardando o campo Renavam.")
                renavam_input = wait_for_element(driver, By.ID, renavam_input_id)
                renavam_input.clear()
                renavam_input.send_keys(renavam)
                print("[INFO] Renavam preenchido.")

                # Aguarda botão "Consultar" e clica
                print("[DEBUG] Aguardando botão Consultar.")
                consultar_button = wait_for_element(driver, By.ID, consultar_button_id)
                consultar_button.click()
                print("[INFO] Consulta enviada.")

                # Aguarda botão de download e clica
                print("[DEBUG] Aguardando botão Download.")
                download_button = wait_for_element(driver, By.ID, download_button_id)
                download_button.click()
                print("[INFO] Download iniciado.")

                # Aguarda tempo para garantir o download
                time.sleep(5)

            except TimeoutException as e:
                print(f"[ERROR] Tempo excedido ao processar: {e}")
                continue
            except StaleElementReferenceException as e:
                print(f"[ERROR] Elemento recriado, tentando novamente: {e}")
                # Tenta localizar o elemento novamente
                try:
                    renavam_input = wait_for_element(driver, By.ID, renavam_input_id)
                    renavam_input.clear()
                    renavam_input.send_keys(renavam)
                except Exception as retry_error:
                    print(f"[ERROR] Falha ao tentar novamente: {retry_error}")
                    continue

    finally:
        print("[INFO] Finalizando o WebDriver.")
        driver.quit()

if __name__ == "__main__":
    main()

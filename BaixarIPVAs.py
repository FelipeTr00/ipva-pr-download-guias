import csv
import datetime
import time
import os
import shutil
import requests
import pandas as pd
import OCRapi
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException, TimeoutException

# DECLARACAO DE VARIAVEIS #

# URL base
urlBase = "https://www.contribuinte.fazenda.pr.gov.br/ipva/faces"

# Caminho completo para a planilha com os dados para realizar a busca dos IPVAs
fileFullPath = r"C:\Users\labreu\Downloads\0_IPVA_PR.xlsx"
# Folha de dados da planilha
sheet = "Dados"

# Pasta para download do arquivo
pastaDefDownload = r"C:\Users\labreu\Downloads"
# Nome padrão do arquivo baixado
NomePadraoArquivo = "grpr.pdf"
# Nome padrão do arquivo captcha
NomePadraoArquivoCaptcha = "captchas/captcha_#RENAVAM#_#PLACA#.png"
# Pasta para salvar o arquivo gerado após o download
pastaFinal = "C:/Users/labreu/Downloads"
# Novo nome do arquivo pdf da guia de pagamento
newFileName = "guiaCotaUnicaIPVA_#DATA#_#RENAVAM#_#PLACA#.pdf"
# Local e nome padrão do arquivo baixado
oldFilePath = pastaDefDownload + "/" + NomePadraoArquivo
# Novo local e nome do arquivo guardado
newFilePath = pastaFinal + "/" + newFileName

# INICIA CODIGO #

# Configura as opções do Chrome
options = webdriver.ChromeOptions()
#options.add_argument("--disable-web-security")
#options.add_argument("--allow-running-insecure-content")
#options.add_argument("test-type")
### Configura Chrome para iniciar maximizado
options.add_argument("--start-maximized")
### Configura Chrome para aguardar o carregamento completo da página
options.page_load_strategy = 'normal'
### Configura o Chrome para ignorar falhas de certificado (importante para não aparecer mensagens que impedirão prosseguir)
options.add_argument("--ignore-certificate-errors")
### Prepara para definir o diretório para baixar o arquivo CSV
prefs = {
	"download.default_directory" : pastaDefDownload, \
	"download.prompt_for_download": False, \
	"download.directory_upgrade": True, \
	"safebrowsing.enabled": False
}
### Configura as preferências, neste caso, o diretório preferencial para download
options.add_experimental_option("prefs", prefs)

# Inicia o driver do Chrome
driver = webdriver.Chrome(options=options)

# Lê a planilha com os Renavams
dfs = pd.read_excel(fileFullPath, sheet_name=sheet)

# Quantidade de itens para download
qnt = len(dfs)

# Aqui vai começar o loop para baixar os arquivos
i = 1
#print(dfs.head(10))
for row in dfs.iterrows():
	#if i == 6:
	#	break
	finalPlaca = row[1]["FinalPlaca"]
	renavam = str(row[1]["Renavam"])
	placa = row[1]["Placa"]
	dataVenc = row[1]["Data vencimento"]
	diaVenc = str(row[1]["Data vencimento"].day)

	# Variaveis para cada loop
	nomeArquivoCaptcha = NomePadraoArquivoCaptcha.replace("#RENAVAM#", renavam).replace("#PLACA#", placa)

	urlInicio = urlBase + "/home"

	# Navega para a página inicial
	driver.get(urlInicio)
	time.sleep(2)

	urlInicio = driver.current_url

	# Encontra o campo Renavam e digita o renavam
	elem = driver.find_element(By.ID, "pt1:r1:0:r2:0:ig1:it1::content")
	elem.clear()
	elem.send_keys(renavam)

	# Encontra o campo data de pagamento e digita a data de vencimento
	select_element = driver.find_element(By.NAME, 'pt1:r1:0:r2:0:ig1:soc1')
	select = Select(select_element)
	select.select_by_visible_text(diaVenc)

	elem = driver.find_element(By.ID, "pt1:r1:0:r2:0:ig1:it2::content")
	elem.click()
	time.sleep(1)

	t = 1
	captchaOK = False
	while ((t < 6) and (not captchaOK)):
		print("***** i: " + str(i) + "/" + str(qnt) + "; t: " + str(t) + "/5 *****")
		# Encontra o captcha e tira um screenshot para poder enviar para a API que reconhece as letras via OCR
		elem = driver.find_element(By.ID, "pt1:r1:0:r2:0:ig1:captcha")
		nomeArquivoScreenShotCaptcha = pastaDefDownload + "/" + nomeArquivoCaptcha
		elem.screenshot(nomeArquivoScreenShotCaptcha)

		# Chamar a API OCR
		retornoCaptcha = OCRapi.ocr_imagem(nomeArquivoCaptcha, nomeArquivoScreenShotCaptcha).lower().replace(" ", "")
		print("Renavam: " + renavam + "; Placa: " + placa + "; dia do vencimento: " + diaVenc + "; captcha: " + retornoCaptcha)

		# Encontra o elemento textbox para preencher o captcha
		elem = driver.find_element(By.ID, "pt1:r1:0:r2:0:ig1:it2::content")
		elem.clear()
		elem.send_keys(retornoCaptcha)

		# Encontra o elemento botão "Consultar" e clica nele
		elem = driver.find_element(By.ID, "pt1:r1:0:r2:0:ig1:b1")
		elem.click()

		# Tenta identificar se houve mensagem de erro, tentando encontrar o botão de "OK" dela
		try:
			# Clica em OK na mensagem
			elem = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "d1_msgDlg_cancel")))
			elem.click()
			# Limpa o campo do captcha
			elem = driver.find_element(By.ID, "pt1:r1:0:r2:0:ig1:it2::content")
			elem.clear()
			# Clica em "Recarregar imagem" do captcha
			elem = driver.find_element(By.ID, "pt1:r1:0:r2:0:ig1:cb2")
			elem.click()
			# Marca que o captcha não foi superado
			captchaOK = False
		except:
			# Se não houve mensagem de erro (o botão "OK" dela não apareceu)
			# Marca que o captcha foi superado
			captchaOK = True
			# Tenta verificar se o elemento nome do proprietário está presente na página
			try:
				elem = WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.ID, "pt1:r1:0:ot2")))
			except (NoSuchElementException, TimeoutException):
				# Trata as excessões por não ter encontrado o link clicável para download da guia
				encontrouElem = False
			finally:
				# Se encontrou o link para download da guia
				if encontrouElem:
					captchaOK = True
					# Tenta encontrar o elemento link da guia para download e, quando ele estiver disponível para clique, clica nele 
					try:
						elem = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "pt1:r1:0:tbCu:0:lnkCu")))
						elem.click()
						time.sleep(2)
						# Define um novo nome do arquivo da guia PDF
						finalFilePath = newFilePath.replace("#DATA#", dataVenc.strftime("%Y-%m-%d")).replace("#RENAVAM#", renavam).replace("#PLACA#", placa)
						# Move o arquivo da pasta de Download para a pasta final, renomeando-o
						shutil.move(oldFilePath, finalFilePath)
					except NoSuchElementException:
						# Trata a excessão de quando o link para download da guia não é encontrado
						print("Link não encontrado!")
					except:
						# Informa qualquer outro erro que tenha dado
						print("Ocorreu outro erro!")
		# Incrementa o contador de tentativas de passar do captcha
		t += 1
	# Incrementa o contador de itens para download
	i += 1

# Aguarda 5s
time.sleep(5)

# Finaliza o driver do Chrome
driver.close()
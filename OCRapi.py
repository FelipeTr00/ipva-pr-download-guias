import requests

#Create an account on https://ocr.space/ocrapi
api_key1 = "K11111111111111"
api_key2 = "K22222222222222"
api_key3 = "K33333333333333"
api_key4 = "K44444444444444"

def req(imageName, imagePath, apiKey):
    url = "https://api.ocr.space/parse/image"
    payload = {"OCREngine": "2", "isTable": "false"}
    files = [("file",(imageName,open(imagePath,"rb"),"image/png"))]
    headers = {"apikey": api_key1}
    response = requests.request("POST", url, headers=headers, data=payload, files=files)
    myJson = response.json()
    return myJson

def ocr_imagem(imageName, imagePath):
    
    myJson = req(imageName, imagePath, api_key1)
    print("apikey1: " + api_key1)
    print(myJson)
    try:
        retorno = myJson["ParsedResults"][0]["ParsedText"]
    except:
        myJson = req(imageName, imagePath, api_key2)
        print("apikey2: " + api_key2)
        print(myJson)
        try:
            retorno = myJson["ParsedResults"][0]["ParsedText"]
        except:
            myJson = req(imageName, imagePath, api_key3)
            print("apikey3: " + api_key3)
            print(myJson)
            try:
                retorno = myJson["ParsedResults"][0]["ParsedText"]
            except:
                myJson = req(imageName, imagePath, api_key4)
                print("apikey4: " + api_key4)
                print(myJson)
                try:
                    retorno = myJson["ParsedResults"][0]["ParsedText"]
                except:
                    retorno = "erro!"

    return retorno
from selenium import webdriver

# Configuração para Microsoft Edge
    options = webdriver.EdgeOptions()
    
    # Configurações gerais
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-software-rasterizer")
    options.add_argument("--start-maximized")
    options.add_argument("--disable-cache")
    options.add_argument("--disable-application-cache")
    return webdriver.Edge(options=options)

# Configuração para Google Chrome
#     options = webdriver.ChromeOptions()
    
#     options.add_argument("--disable-gpu")
#     options.add_argument("--disable-software-rasterizer")
#     options.add_argument("--start-maximized")
#     options.add_argument("--disable-cache")
#     options.add_argument("--disable-application-cache")
#     return webdriver.Chrome(options=options)

# Configuração para Mozilla Firefox
#     options = webdriver.FirefoxOptions()
    
#     options.add_argument("--disable-gpu")
#     options.set_preference("browser.cache.disk.enable", False)
#     options.set_preference("browser.cache.memory.enable", False)
#     options.set_preference("browser.cache.offline.enable", False)
#     options.set_preference("network.http.use-cache", False)
#     return webdriver.Firefox(options=options)

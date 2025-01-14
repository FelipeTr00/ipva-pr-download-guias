from selenium import webdriver

def configure_driver():
    options = webdriver.EdgeOptions()
    # options = webdriver.ChromeOptions()
    # options = webdriver.FirefoxOptions()

    # Configurações
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-software-rasterizer")
    options.add_argument("--start-maximized")
    # options.add_argument("--window-size=960,1080")
    # options.add_argument("--window-position=0,0")
    options.add_argument("--disable-cache")
    options.add_argument("--disable-application-cache")
    return webdriver.Edge(options=options)

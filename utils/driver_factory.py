import os
from dotenv import load_dotenv
from seleniumwire import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions

def create_driver(browser_type="chrome", use_proxy=True, headless=False):
    load_dotenv()

    proxy_options = None
    if use_proxy:
        proxy_host = os.getenv("GEONODE_HOST")
        proxy_port = os.getenv("GEONODE_PORT")
        username = os.getenv("GEONODE_USERNAME")
        password = os.getenv("GEONODE_PASSWORD")

        proxy_options = {
            'proxy': {
                'http': f'http://{username}:{password}@{proxy_host}:{proxy_port}',
                'https': f'https://{username}:{password}@{proxy_host}:{proxy_port}',
            },
            'no_proxy': 'localhost,127.0.0.1'
        }

    if browser_type == "chrome":
        options = ChromeOptions()
        options.add_argument('--disable-gpu')
        options.add_argument('--ignore-certificate-errors')
        if headless:
            options.add_argument('--headless=new')

        driver = webdriver.Chrome(seleniumwire_options=proxy_options, options=options)

        driver.set_window_position(-1440, 0) 
        driver.maximize_window()

        return driver

    elif browser_type == "firefox":
        options = FirefoxOptions()
        options.headless = headless
        driver = webdriver.Firefox(seleniumwire_options=proxy_options, options=options)

        # Open on left monitor
        driver.set_window_position(-1440, 0) 
        driver.maximize_window()

        return driver

    else:
        raise ValueError("browser_type must be 'chrome' or 'firefox'")

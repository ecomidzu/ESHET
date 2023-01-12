from seleniumwire import webdriver
from selenium.webdriver.chrome.service import Service
import time
from tqdm import tqdm
import random
import pandas as pd

class UseSelenium:
    def __init__(self, url: list, filename: list, fol_dir: str):
        self.url = url
        self.filename = filename
        self.fol_dir = fol_dir

    def save_page(self):

        options = webdriver.ChromeOptions()
        options.add_argument(f"user-agent={'Chrome/108.0.0.0'}")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("--headless")
        hos=None
        options_proxy = {
            'proxy': {
                'https': hos,
                'no_proxy': 'localhost,127.0.0.1:8080'
            }
        }

        s = Service(executable_path="/lib/chromedriver")

        driver = webdriver.Chrome(options=options, service=s, seleniumwire_options=options_proxy)

        try:
            i=0
            for k in tqdm(self.url):
                driver.get(k)
                time.sleep(1)
                driver.execute_script("window.scrollTo(5,4000);")
                time.sleep(1)
                html = driver.page_source
                with open(self.fol_dir + '/' + self.filename[i], 'w', encoding='utf-8') as f:
                    f.write(html)
                i+=1
        except Exception as ex:
            print(ex)
        finally:
            driver.close()
            driver.quit()
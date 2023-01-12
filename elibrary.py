from seleniumwire import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.webdriver.support import expected_conditions as EC
import selenium
from selenium.webdriver.common.by import By
import time
import random
import pandas as pd
from tqdm import tqdm


class WorkFlow:
    def __init__(self, query: str, params: dict = {}, pages: int = 1):
        self.query = query
        self.params = params
        self.pages = pages

    def make_query(self):
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
            driver.get('https://www.elibrary.ru/querybox.asp?scope=newquery')
            time.sleep(1)
            a = driver.find_element(by=By.TAG_NAME, value='textarea')
            a.click()
            time.sleep(1)
            a.send_keys(self.query)
            driver.execute_script("javascript:query_message()")
            time.sleep(1)
            for i in tqdm(range(self.pages)):
                html = driver.page_source
                with open('pages/' + str(i)+'.html', 'w', encoding='utf-8') as f:
                    f.write(html)
                if i-self.pages!=1:
                    driver.get('https://www.elibrary.ru/query_results.asp?pagenum=' + str(i+2))
        except Exception as ex:
            print(ex)
        finally:
            driver.close()
            driver.quit()

def main():
    a = WorkFlow(query='Экономика', pages=2)
    a.make_query()

if __name__ == '__main__':
    main()
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

import pandas as pd
import time, logging, warnings, sys

warnings.simplefilter(action='ignore', category=FutureWarning)
logging.basicConfig(filename="logStocks.log", level=logging.INFO, format='%(asctime)s %(levelname)-8s %(message)s')

class GetStocks:
    ''' Return the stocks from the desired region on a csv file '''
    def __init__(self, region: str):
        '''
            Parameters:
                - region: The name of the desired region
        '''
        self.region = region
        self.driver = self.create_driver()

    def create_driver(self):
        '''
            Description:
                Creates the Chrome driver
        '''
        try:
            chrome_options = Options()
            chrome_options.add_argument('--log-level=3')
            driver = webdriver.Chrome(options=chrome_options)
            return driver
        except Exception as e:
            _, _, exc_tb = sys.exc_info()
            print(f"ERROR: {e}. LINE: {exc_tb.tb_lineno}")
            logging.error(f"ERROR: {e}. LINE: {exc_tb.tb_lineno}")
            return None
    
    def main(self):
        '''
            Description:
                Controls the crawler and creates the final file with the Stocks
        '''

        self.driver.get('https://finance.yahoo.com/screener/new')

        logging.info('Searching the region....')

        WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//*[@id='screener-criteria']/div[2]/div[1]/div[1]/div[1]/div/div[2]/ul/li[1]/button"))).click()
        WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//*[@id='screener-criteria']/div[2]/div[1]/div[1]/div[1]/div/div[2]/ul/li[1]/button"))).click()

        WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//*[@id='dropdown-menu']/div[1]/div[1]/div[1]/input"))).clear()
        WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//*[@id='dropdown-menu']/div[1]/div[1]/div[1]/input"))).send_keys(self.region)
        time.sleep(2)

        try: 
            WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//*[@id='dropdown-menu']/div[1]/div[2]/ul/li/label/input"))).click()
        except:
            logging.error('Region does not exist, please verify')
            return

        WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//*[@id='screener-criteria']/div[2]/div[1]/div[3]/button[1]"))).click()

        time.sleep(5)

        logging.info('Getting the stocks...')

        table = self.driver.find_element("xpath","//*[@id='screener-results']/div[1]/div[2]/div[1]/table").get_attribute("outerHTML")
        df_final = pd.read_html(table)[0]
        df_final = df_final.iloc[:, :3]

        while True:
            try:
                WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//*[@id='screener-results']/div[1]/div[2]/div[2]/button[3]"))).click()
            except:
                logging.info('Stocks finished!')
                break
            else:
                time.sleep(2)
                table = self.driver.find_element("xpath","//*[@id='screener-results']/div[1]/div[2]/div[1]/table").get_attribute("outerHTML")
                df = pd.read_html(table)[0]
                df = df.iloc[:, :3]
                df_final = pd.concat([df_final, df])

        df_final.to_csv(f'stocks_{self.region}.csv')

        logging.info('File exported!')

        self.driver.quit()

if __name__ == '__main__':
    GetStocks('Czechia').main()
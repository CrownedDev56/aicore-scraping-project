from dataclasses import dataclass
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from time import sleep

from tqdm import tqdm
from selenium.common.exceptions import NoSuchElementException, TimeoutException

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC



@dataclass()
class MensWatches():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("disable-infobars")
    options.add_argument("--disable-extensions")
    options.add_argument("--start-maximized")
    options = options
    _URL = "https://www.goldsmiths.co.uk/"
    driver = webdriver.Chrome(options=options)
    driver.get(_URL)

    def accept_cookies(self) -> None:
        cookies_button = self.driver.find_element_by_xpath('//div[@id="cookie-accept"]')
        cookies_button.click()

    def mens_watch_nav(self) -> None:
        '''
        This method will navigate to the mens watch section of the website
        '''

        actions = ActionChains(self.driver)
        sleep(3)

        try: 
            self.driver.find_element_by_xpath('/html/body/main/div[1]/div[3]/div/div[1]/div[2]').click() 
            sleep(1) 
            self.driver.find_element_by_xpath('/html/body/main/div[1]/div[5]/div[2]/ul/li[6]/a').click()
            sleep(1) 
            self.driver.find_element_by_xpath('/html/body/main/div[1]/div[5]/div[2]/ul/li[6]/ul/li[2]/a').click()
            sleep(1) 
            self.driver.find_element_by_xpath('/html/body/main/div[1]/div[5]/div[2]/ul/li[6]/ul/li[2]/ul/li[2]/a').click() 
        except NoSuchElementException:
            menu_hover = self.driver.find_element_by_xpath('/html/body/main/div[1]/div[4]/div/div/div/div/ul/li[5]') 
            
            actions.move_to_element(menu_hover).perform() 
            sleep(1) 
            self.driver.find_element_by_xpath('/html/body/main/div[1]/div[4]/div/div/div/div/ul/li[5]/div/div/div/div[1]/div[2]/a').click()

    def load_all(self, n_pages=1) -> None:
        '''
        This method will load all watches in the webpage
        If n_pages is 0, it will load all pages
        Otherwise, it will load n_pages
        '''

        # waits 3 seconds for the page to load before searching for the load more products button
        if n_pages == 0:
            while True:
                sleep(1)
                try:
                    load_more_products = WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable((By.XPATH, '//div[@id="pagination-LoadMore"]')))
                    load_more_products.click()
                except TimeoutException:
                    break
        else:
            for _ in range(n_pages):
                sleep(1)
                try:
                    load_more_products = WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable((By.XPATH, '//div[@id="pagination-LoadMore"]')))
                
                    load_more_products.click()
                except TimeoutException:
                    break

    def get_links(self) -> list:
        '''
        This method will get all the links on the page
        '''
        links = []
        lostlinks = []
        grid_watch = self.driver.find_element_by_xpath('//div[@class="gridBlock row"]')
        watch_list = grid_watch.find_elements_by_xpath('./div')
        print('Collecting Links')
        for i,  watch in enumerate(tqdm(watch_list)):
            try:
                link = watch.find_element_by_xpath('.//a').get_attribute('href')
                links.append(link)
            except NoSuchElementException:
                
                lostlinks.append(link)
        print('Link Collection Complete')
        for i in lostlinks:
            print(f'Lost link: {i}')
        return links

    def get_image_source(self, link: str) -> str:

        if self.driver.current_url != link:
            self.driver.get(link)
            sleep(1)

        src = self.driver.find_element_by_class_name('zoomImg').get_attribute('src')

        return src

    def get_properties(self, link):
        '''
        Go to the link and get the properties of the watch

        '''
        data = {"product_name": None, "product_price": None, "product_code": None, "brand": None, "guarantee": None,
                        "watch_markers": None, "water_resistant": None, "strap_material": None,
                        "recipient": None, "movement": None, "dial_colour": None,
                        "case_material": None, "diameter": None, "brand_collections": None
                        }
        
        if self.driver.current_url != link:
            self.driver.get(link)
            sleep(0.5)

        product_name_elem = self.driver.title
        data["product_name"] = product_name_elem[:-13]

        product_price_elem = self.driver.find_element_by_class_name('productPrice')

        data["product_price"] = product_price_elem.text[1:]

        spec_label = self.driver.find_elements_by_class_name('specLabel')
        spec_value = self.driver.find_elements_by_class_name('specValue')

        for label, value in zip(spec_label, spec_value):
            label_key = label.text
            label_key = label_key.lower().split()
            label_key = '_'.join(label_key)

            if label_key in data:
                data[label_key] = value.text

        #for k, v in data.items():
        #    if len(v) != len(data['product_name']) or v == '':
        #        data[k].append(None)
        return data

   

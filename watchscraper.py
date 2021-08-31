from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
import pandas as pd
from time import sleep 
from selenium.common.exceptions import NoSuchElementException
import psycopg2
from sqlalchemy import create_engine




class MensWatches():
    


    def __init__(self, URL="https://www.goldsmiths.co.uk/"):
        self.DATABASE_TYPE = 'postgresql'
        self.DBAPI = 'psycopg2'
        self.HOST = 'localhost'
        self.USER = 'postgres'
        self.PASSWORD = ''
        self.DATABASE = 'aicore_project'
        self.PORT = '5432'

        
        
        self.driver = webdriver.Chrome()
        self.driver.get(URL)
        
        sleep(1)


    def accept_cookies(self):
        cookies_button = self.driver.find_element_by_xpath('//div[@id="cookie-accept"]')
        cookies_button.click()


    def mens_watch_nav(self):
        '''
        This method will navigate to the mens watch section of the website
        '''
       

        actions = ActionChains(self.driver)
        ham_menu = self.driver.find_element_by_xpath('/html/body/main/div[1]/div[3]/div/div[1]/div[2]')
        ham_menu_1 = self.driver.find_element_by_xpath('/html/body/main/div[1]/div[5]/div[2]/ul/li[6]/a')
        ham_menu_2 = self.driver.find_element_by_xpath('/html/body/main/div[1]/div[5]/div[2]/ul/li[6]/ul/li[2]/a')
        Ham_menu_3_mens_w = self.driver.find_element_by_xpath('/html/body/main/div[1]/div[5]/div[2]/ul/li[6]/ul/li[2]/ul/li[2]/a')

        menu_hover = self.driver.find_element_by_xpath('/html/body/main/div[1]/div[4]/div/div/div/div/ul/li[5]')
        menu_hover_1_mens_w = self.driver.find_element_by_xpath('/html/body/main/div[1]/div[4]/div/div/div/div/ul/li[5]/div/div/div/div[1]/div[2]/a')
        
        try:
            ham_menu.click()
            sleep(0.5)
            ham_menu_1.click()
            sleep(0.5)
            ham_menu_2.click()
            sleep(0.5)
            Ham_menu_3_mens_w.click()
        except:
            actions.move_to_element(menu_hover).perform()
            sleep(0.5)
            menu_hover_1_mens_w.click()


    def load_all(self, n_pages=1):
        '''
        This method will load all watches in the webpage
        If n_pages is 0, it will load all pages
        Otherwise, it will load n_pages
        '''
        if n_pages == 0:
            last_height = self.driver.execute_script("return document.body.scrollHeight")
            while True:
                # Scroll down to bottom
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                sleep(1)
                load_more_products = self.driver.find_element_by_xpath('//div[@id="pagination-LoadMore"]') 
                self.driver.execute_script("arguments[0].click();", load_more_products)
                # Wait to load page
                sleep(1)
                # Calculate new scroll height and compare with last scroll height
                new_height = self.driver.execute_script("return document.body.scrollHeight")
                if new_height == last_height:
                    break
                last_height = new_height
        else:
            last_height = self.driver.execute_script("return document.body.scrollHeight")
            for _ in range(n_pages):
                # Scroll down to bottom
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                sleep(1)
                load_more_products = self.driver.find_element_by_xpath('//div[@id="pagination-LoadMore"]') 
                self.driver.execute_script("arguments[0].click();", load_more_products)
                # Wait to load page
                sleep(1)
                # Calculate new scroll height and compare with last scroll height
                new_height = self.driver.execute_script("return document.body.scrollHeight")
                if new_height == last_height:
                    break
                last_height = new_height
        

    def get_links(self):
        '''
        This method will get all the links on the page
        '''
        links = []
        grid_watch = self.driver.find_element_by_xpath('//div[@class="gridBlock row"]')
        watch_list = grid_watch.find_elements_by_xpath('./div')
        for watch in watch_list:
            try:
                link = watch.find_element_by_xpath('.//a').get_attribute('href')
                links.append(link)
            except NoSuchElementException:
                pass
        return links
    
    def get_properties(self, links):
        print(len(links))
        '''
        Go to the link and get the properties of the watch

        '''
        engine = create_engine(f"{self.DATABASE_TYPE}+{self.DBAPI}://{self.USER}:{self.PASSWORD}@{self.HOST}:{self.PORT}/{self.DATABASE}")

        data = {"product_name": [], "product_price": [], "product_code" : [],"brand" : [], "guarantee": [],
                "watch_markers": [],"water_resistant": [], "strap_material": [],
                "recipient": [],"movement": [], "dial_colour": [],
                "case_material": [], "diameter" : [], "brand_collections": []
                }
        for link in links:
            self.driver.get(link)

            try:
                product_name_elem = self.driver.title
                data["product_name"].append(product_name_elem[:-13])

                product_price_elem = self.driver.find_element_by_class_name('productPrice')
                    
                data["product_price"].append(product_price_elem.text[1:])

                spec_label = self.driver.find_elements_by_class_name('specLabel')
                spec_value = self.driver.find_elements_by_class_name('specValue')

                for label, value in zip(spec_label, spec_value):
                    if label.text == "PRODUCT CODE":
                        data["product_code"].append(value.text)
                            
                    elif label.text == "GUARANTEE":
                        data["guarantee"].append(value.text)
                            
                    elif label.text == "BRAND":
                        data["brand"].append(value.text)
                    
                                    
                    elif label.text == "WATCH MARKERS":
                        data["watch_markers"].append(value.text)

                    elif label.text == "WATER RESISTANT":
                        data["water_resistant"].append(value.text[:-7])

                    elif label.text == "STRAP MATERIAL":
                        data["strap_material"].append(value.text)

                    elif label.text == "RECIPIENT":
                        data["recipient"].append(value.text)

                    elif label.text == "MOVEMENT":
                        data["movement"].append(value.text)

                    elif label.text == "DIAL COLOUR":
                        data["dial_colour"].append(value.text)
                    elif label.text == "CASE MATERIAL":
                        data["case_material"].append(value.text)

                    elif label.text == "DIAMETER":

                        data["diameter"].append(value.text[:-2])

                    elif label.text == "BRAND COLLECTIONS":
                        data["brand_collections"].append(value.text)
                        
                for k, v in data.items():
                    if len(v) != len(data['product_name']) or v == '':
                        data[k].append(None)
                        


                df = pd.DataFrame.from_dict(data)
                df.fillna
                df.to_csv('mens_watches_py.csv', index=False) 
                df.to_sql('mens_watches', engine, if_exists='replace')

            except:
                pass
        
        

           
     
scrapper = MensWatches()
scrapper.accept_cookies()
scrapper.mens_watch_nav()
scrapper.load_all(30)
links = scrapper.get_links()
scrapper.get_properties(links)
from .watchscraper import MensWatches
from .datahandler import DataHandler
from time import sleep
from selenium.common.exceptions import NoSuchElementException
from tqdm import tqdm


scraper = MensWatches()
store = DataHandler()
pages = int(input("How many pages would you like to load? "))
print('Starting Scraper...')
scraper.accept_cookies()
scraper.mens_watch_nav()
scraper.load_all(pages)
sleep(0.5)
links = scraper.get_links()
watch_data = []

print('Collecting Data...')
for i, link in enumerate(tqdm(links)):
   
    scraper.driver.get(link)
    sleep(0.5)
    try:
        src = scraper.get_image_source(link)
        
        store.download_images(src, i)
        watch_data.append(scraper.get_properties(link))
       
    except NoSuchElementException:
        pass

store.store_as_csv(watch_data)
try:
    store.store_data_online(watch_data)
except FileNotFoundError:
    print("Database server details not found...")

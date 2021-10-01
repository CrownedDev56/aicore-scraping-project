
from scraper.watchscraper import MensWatches
import unittest
from time import sleep


class WatchScraperTest(unittest.TestCase):

    def setUp(self):
        self.scraper = MensWatches()
        self.driver = self.scraper.driver
        self.url = self.scraper._URL
        self.driver.get(self.url)

    def test_website_link(self):
        self.assertIn("www.goldsmiths.co.uk", self.driver.current_url)

    def test_minimized_navigation(self):
        navigation = MensWatches()
        navigation.mens_watch_nav()
        self.assertIn("www.goldsmiths.co.uk/c/Watches/Mens-Watches", self.driver.current_url)
    
    def test_get_image_source(self):
        link = "https://www.goldsmiths.co.uk/Omega-Speedmaster-Professional-Moonwatch-First-Watch-On-The-Moon-Certified-By-NASA-O31130423001005/p/17331157"
        img_source = self.scraper.get_image_source(link)
        image = "https://content.thewosgroup.com/productimage/17331157/17331157_1.jpg?impolicy=zoom"

        self.assertEqual(img_source, image)
        
    def test_get_properties(self):
        link = "https://www.goldsmiths.co.uk/Omega-Speedmaster-Professional-Moonwatch-First-Watch-On-The-Moon-Certified-By-NASA-O31130423001005/p/17331157"
        property_source = self.scraper.get_properties(link)
        returned_property = {'product_name': 'Omega Speedmaster Professional Moonwatch First Watch On The Moon Certified By NASA O31130423001005', 'product_price': '4,260.00', 'product_code': '17331157', 'brand': 'Omega', 'guarantee': 'Omega 5 Year Guarantee', 'watch_markers': 'Batons', 'water_resistant': '50 Metres', 'strap_material': 'Stainless Steel', 'recipient': 'For Him', 'movement': 'Manual Winding', 'dial_colour': 'Black', 'case_material': 'Stainless Steel', 'diameter': '42mm', 'brand_collections': 'Speedmaster'}
        self.assertEqual(property_source, returned_property)
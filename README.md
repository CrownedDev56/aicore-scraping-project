# aicore-scraping-project


init(self, URL): the self instance varibale contains the instance of the class where it contains the Database details, where it uses ther self.driver variable to create a webdriver for chrome using the URL

accept_cookies(self) locates and clicks the cookies button when visible

mens_watch_nav(self) navigates to mens watches page, through either the dropdown menu or the hamburger menu

load_all(self, n_pages) scrolls to the bottom of the page clicking the load more button displaying more products, this loops based on the n_pages defined or untill unable if n_pages is 0

get_links(self) gets the links of all the visible watches displayed, appending them to a list, which is then returned

get_properties(self, links)

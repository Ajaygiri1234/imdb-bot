from robot.libraries.BuiltIn import BuiltIn

from libraries.Communicate import RunItem
from libraries.Constants import COMPLETED, ERROR
from libraries.SetupError import setup_error
from Utils import log_to_console
from Utils import log_to_console as print
from RPA.Browser.Selenium import Selenium
import time



class Imdbbot(object):
    def __init__(self) -> None:
        self.driver=Selenium()
    def search_movies(self):
        movie_name="the matrix"
        url=f"https://www.imdb.com/find?q={movie_name}&s=tt&ttype=ft&exact=true"
        xpath_date =f"//td[@class='result_text']//a[translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz') =   '{movie_name}'   ]/.."
        xpath_link=f"//td[@class='result_text' and a[   translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz') =   '{movie_name}'   ]]/a"
        self.driver.open_chrome_browser(url=url)
        list_of_date=self.driver.find_elements(locator=xpath_date)
        list_of_link=self.driver.find_elements(locator=xpath_link)
        movie_link=""

        max_date=1800
        for i in range(len(list_of_date)):
            date=list_of_date[i].text.split(" ")[-1][1:-1]
            if int(date)>max_date:
                max_date=int(date)
                movie_link=list_of_link[i]
        
        log_to_console( movie_link.click())
        time.sleep(5)
        self.get_details()

    def get_details(self):
        

        detail={}
        rating=self.driver.find_element(locator='//div[@data-testid="hero-rating-bar__aggregate-rating__score"]/span[@class]').text
        count=0
        
        while(1):
            try:
                storyline=self.driver.find_element(locator='//div[@data-testid="storyline-plot-summary"]//div[@class="ipc-html-content-inner-div"]').text
                break

            except:
                
                
                time.sleep(5)
                if count==12:
                    storyline=''
                    break
                count+=1

        genre_list=self.driver.find_elements(locator='//li[@data-testid="storyline-genres"]//ul/li')
        genre=[]
        for i in genre_list:
            genre.append(i.text)
        


        log_to_console(rating)
        log_to_console(storyline)
        log_to_console(genre)
        
        self.driver.click_element(locator='//li[@data-testid="storyline-taglines"]/a')
        time.sleep(2)
        taglines=self.driver.find_elements(locator='//div[ @id="taglines_content"]/div[@class="soda odd" or @class="soda even"]')
        tagline=[]
        for i in taglines:
            tagline.append(i.text)

        print(tagline)
        
















        # log_to_console(list_of_result[3].find_element_by_tag_name('a').)
        # time.sleep(3)
        # max_date=1800
        # movie_link : self.driver.webdriver.remote.webelement.WebElement
        # for each_result in range(len_of_result):
           
        #     name=each_result.find_element_by_tag_name('td')
        #     log_to_console((name.text))
        #     if name.text.lower()=="titanic":
        #         date=int(each_result.text.split(" ")[-1][1:-1])
        #         log_to_console(date)
        #         if date>max_date:
        #             max_date=date
        #             movie_link=name
        # movie_link.click()
        
            

        



        #     #log_to_console(each_result.text.split('\n')[0][-1])
        

        # # log_to_console(dir(a[0]))
        # # log_to_console(("A"))#.get_attribute('href')
        # # elem=a[0].find_element_by_tag_name('a').click()
        # #elem.click()
        # time.sleep(5)
        

#  ['__class__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__gt__', '__hash__'
# , '__init__', '__init_subclass__', '__le__', '__lt__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__',
#  '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', '_execute', '_id', '_parent', '_upload', '_w3c', 'clear', 
# 'click', 'find_element', 'find_element_by_class_name', 'find_element_by_css_selector', 'find_element_by_id', 'find_element_by_link_text', 
# 'find_element_by_name', 'find_element_by_partial_link_text', 'find_element_by_tag_name', 'find_element_by_xpath', 'find_elements',
#  'find_elements_by_class_name', 'find_elements_by_css_selector', 'find_elements_by_id', 'find_elements_by_link_text',
#  'find_elements_by_name', 'find_elements_by_partial_link_text', 'find_elements_by_tag_name', 'find_elements_by_xpath', 
# 'get_attribute', 'get_property', 'id', 'is_displayed', 'is_enabled', 'is_selected', 'location',
#  'location_once_scrolled_into_view', 'parent', 'rect', 'screenshot', 'screenshot_as_base64', 'screenshot_as_png',
#  'send_keys', 'size', 'submit', 'tag_name', 'text', 'value_of_css_property']      
    #    

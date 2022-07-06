import pandas
from robot.libraries.BuiltIn import BuiltIn
from RunItems import post_complete_run_item,post_error_run_item
from BotLogger import BotLogger
from libraries.Communicate import RunItem
from libraries.Constants import COMPLETED, ERROR
from libraries.SetupError import setup_error
from Utils import log_to_console
from Utils import log_to_console as print
from RPA.Browser.Selenium import Selenium
import time
from RPA.Excel.Files import Files
import pandas as pd


class Imdbbot(object):
    def __init__(self) -> None:
        self.driver=Selenium()
        self.MovieNotfound=False
        self.logger=BotLogger()
        
    def open(self):
        self.driver.open_chrome_browser(url='https://www.imdb.com/')

    def search_movies(self,movie_name):
        self.MovieNotfound = False
        url=f"https://www.imdb.com/find?q={movie_name}&s=tt&ttype=ft&exact=true"
        xpath_date =f"//td[@class='result_text']//a[translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz') =   '{movie_name}'   ]/.."
        xpath_link=f"//td[@class='result_text' and a[   translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz') =   '{movie_name}'   ]]/a"
        self.driver.go_to(url=url)
        list_of_date=self.driver.find_elements(locator=xpath_date)
        list_of_link=self.driver.find_elements(locator=xpath_link)
        movie_link=""
       
        max_date=1800
        for i in range(len(list_of_date)):
            date_str=list_of_date[i].text.split(" ")[-1][1:-1]
            try:
                date = int(date_str)
                
                if int(date)>max_date:
                    max_date=int(date)
                    movie_link=list_of_link[i]
            except Exception as e:
                print("No date")
        try:
            movie_link.click()
            time.sleep(5)
        except Exception as e:
            self.MovieNotfound = True
            print(e)
        # self.MovieNotfound = False


        

    def get_details(self,movies_list):
        result = {}
        try:
            started_at=BuiltIn().get_time()
            self.open()
            self.logger.logger.info('browser opened successfully')
            log_text=self.logger.get_log_contents()
            post_complete_run_item(started_at=started_at,completed_at=BuiltIn().get_time(),log_text=log_text)
            self.logger.clear_logs()
        except:
            
            return result
        
        for movie in movies_list:
            started_at=BuiltIn().get_time()
            self.logger.logger.info(f"searching exact match {movie}")
            self.search_movies(movie_name=movie)
            
            if self.MovieNotfound:
                self.logger.logger.info(f"exact match of {movie}not found")
                log_text=self.logger.get_log_contents()
                post_error_run_item(started_at=started_at,completed_at=BuiltIn().get_time(),log_text=log_text)
                self.logger.clear_logs()
                continue
                print("Movie not found")
            self.logger.logger.info(f"Exact match of {movie} found")
            rating=self.driver.find_element(locator='//div[@data-testid="hero-rating-bar__aggregate-rating__score"]/span[@class]').text
            self.logger.logger.info(f"rating of {movie} found -->{rating}")
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
            self.logger.logger.info(f"story line of {movie} found ")
            genre_list=self.driver.find_elements(locator='//li[@data-testid="storyline-genres"]//ul/li')
            genre=[]
            for i in genre_list:
                genre.append(i.text)
            

            self.logger.logger.info(f"genre of {movie} is {genre} ")
            
            try:
                self.driver.click_element(locator='//li[@data-testid="storyline-taglines"]/a')
            
                time.sleep(2)
                taglines_object=self.driver.find_elements(locator='//div[ @id="taglines_content"]/div[@class="soda odd" or @class="soda even"]')
                tagline=[]
                for i in taglines_object:
                    tagline.append(i.text)
            except:
                tagline=[self.driver.find_element(locator='//li[@data-testid="storyline-taglines"]//span[not (text()="Taglines")]').text]

            self.logger.logger.info(f"tageline  of {movie} found")

            log_to_console(rating)
            log_to_console(storyline)
            log_to_console(genre)
            print(tagline)
            result.update({movie : {
                
                'rating':rating,
                'storyline': storyline,
                'genre':genre,
                'tagline':tagline,
            }})
            self.logger.logger.info(f"final result")
            log_text=self.logger.get_log_contents()
            report_data={
                'movie_name':movie,
                'rating':rating,
                'storyline': storyline,
                'genre':genre,
                'tagline':tagline,
            }
            post_complete_run_item(started_at=started_at,completed_at=BuiltIn().get_time(),log_text=log_text,report_data=report_data)

        return result





class Excel():
    def __init__(self) -> None:
        self.file=Files()
        self.columns=[]
        self.movies=[]
    def readmovies(self):
        df=pd.read_excel('imdb_data.xlsx')
        # print(list(df['Movie']))
        # print(df.columns)
        self.columns=list(df.columns)
        self.movies = [x.lower() for x in list(df['Movie'])]
        # print(self.movies)
        return self.movies

    def save_result(self,result):
        df=pd.DataFrame.from_dict(result,orient='index')
        df.to_excel('output/output.xlsx',)
        print(df)
        














        

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

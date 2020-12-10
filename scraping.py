#import stuff
from splinter import Browser
from bs4 import BeautifulSoup as soup
#from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import datetime as dt


def scrape_all():
    #initiate headless driver for deployment
    browser = Browser('chrome', executable_path='chromedriver', headless=True)

    news_title, news_paragraph = mars_news(browser)

    #run all scraping functions and store results in dict
    data = {
        'news_title': news_title,
        'news_paragraph': news_paragraph,
        'featured_image': featured_image(browser),
        'facts': mars_facts(),
        'last_modified': dt.datetime.now()
    }

    #stop webdriver and return data
    browser.quit()
    return data


# Setup splinter
#executable_path = {'executable_path': ChromeDriverManager().install()}


def mars_news(browser):
    # Visit the mars nasa news site
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)

    #optional delay for loading the page
    browser.is_element_present_by_css("ul.item_list li.slide", wait_time=1)

    #set up html parser
    html = browser.html
    news_soup = soup(html, 'html.parser')

    #add try/except for error handling
    try:
        #set variable to ul element with item_list class and the li elements belonging to it
        slide_elem = news_soup.select_one('ul.item_list li.slide')

        #user parent element to find the first 'a' tag and save it as 'news_title'
        news_title = slide_elem.find('div', class_='content_title').get_text()

        #use parent element to find paragraph text
        news_p = slide_elem.find('div', class_='article_teaser_body').get_text()

    except AttributeError:
        return None, None
    
    return news_title, news_p



#### Featured Images

def featured_image(browser):

    #visit url
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)

    #find and click the full image button
    full_image_elem = browser.find_by_id('full_image')
    full_image_elem.click()

    #find the more info button and click 
    browser.is_element_present_by_text('more info', wait_time=1)
    more_info_elem = browser.links.find_by_partial_text('more info')
    more_info_elem.click()

    #parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')

    try:
        #find relative image url
        img_url_rel = img_soup.select_one('figure.lede a img').get('src')

    except AttributeError:
        return None

    #use base url to create an absolute url
    img_url = f'https://www.jpl.nasa.gov{img_url_rel}'
    
    return img_url


def mars_facts():

    try:
        #scrape facts table and create dataframe
        df = pd.read_html('http://space-facts.com/mars/')[0]

    except BaseException:
        return None

    #assign columns and set index of df
    df.columns = ['description', 'value']
    df.set_index('description', inplace=True)
        
    #convert dataframe back to html
    return df.to_html()


if __name__ == '__main__':
    #if running as script, print scraped data
    print(scrape_all())





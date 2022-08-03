import pandas as pd
import requests
import pymongo
from splinter import Browser
from bs4 import BeautifulSoup as bs
from webdriver_manager.chrome import ChromeDriverManager

def scrape():
    #setup splinter
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    #setting link
    news_url = 'https://redplanetscience.com/'
    browser.visit(news_url)

    #delay due to slow load time
    browser.is_element_present_by_css('div.list_text', wait_time=5)

    #scrape and store article title/paragraph
    html = browser.html
    soup = bs(html, 'html.parser')
    news_title = soup.find('div', class_='content_title').text
    news_para = soup.find('div', class_='article_teaser_body').text

    #JPL Mars Space Images-Featured Image

    #setting link
    jpl_url = 'https://spaceimages-mars.com/'
    browser.visit(jpl_url)

    #delay due to slow load time
    browser.is_element_present_by_css('div.list_text', wait_time=5)

    #scrape and store img source
    html = browser.html
    soup = bs(html, 'html.parser')
    image_url = jpl_url + soup.find('img', class_='headerimage fade-in')['src']

    #Mars Facts

    #setting link
    fact_url = 'https://galaxyfacts-mars.com/'

    #setting df
    facts_df = pd.read_html(fact_url, header=0,index_col=0)[0]

    #setting df to html and removing new lines
    table = facts_df.to_html()
    table = table.replace('\n', '')

    #Mars Hemispheres

    #setting link
    hemisphere_url = 'https://marshemispheres.com/'
    browser.visit(hemisphere_url)

    #delay due to slow load time
    browser.is_element_present_by_css('div.wrapper', wait_time=5)

    #scrape and store items
    html = browser.html
    soup = bs(html, 'html.parser')
    items = soup.find_all('div',class_='item')

    #loop to get all title names and links
    links = []
    titles = []
    for item in items:
        links.append(hemisphere_url + item.find('a')['href'])
        titles.append(item.find('h3').text.strip())

    #loop to get images for each link
    image_urls = []
    for x in links:
        browser.visit(x)
        html = browser.html
        soup = bs(html, 'html.parser')
        x = hemisphere_url + soup.find('img',class_='wide-image')['src']
        image_urls.append(x)

    #combining title and link
    hemisphere_image_urls = []
    for x in range(0,len(titles)):
        hemisphere_image_urls.append({'title':titles[x],'img_url':image_urls[x]})

    #quit browser
    browser.quit()

    #making dict for scrape data
    data = {}
    data['news_title'] = news_title
    data['news_para'] = news_para
    data['image_url'] = image_url
    data['table'] = table
    data['hemisphere_image_urls'] = hemisphere_image_urls

    return data
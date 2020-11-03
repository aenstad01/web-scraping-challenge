# Dependencies
from splinter import Browser
from bs4 import BeautifulSoup as bs
import requests
import pymongo
import pandas as pd
import time

def init_browser():

    #Set up the ChromeDriver
    executable_path = {'executable_path': 'C:/bin/chromedriver'}
    
    browser = Browser('chrome', **executable_path, headless=False)
    return browser

def scrape():
    browser = init_browser()
    listings  = {}

    #here's the url we want to scrape
    url = 'https://mars.nasa.gov/news/'

    browser.visit(url)

    #wait 5 seconds to ensure the scraper has enough time to find the title & paragraph
    time.sleep(5)
    html = browser.html
    soup= bs(html, 'html.parser')

    try:
        step1 = soup.select_one("ul.item_list li.slide")
        news_title = step1.find("div", class_='content_title').get_text()
        news_p = step1.find("div", class_='article_teaser_body').get_text()
        listings["news_title"] = news_title
        listings["news_p"] = news_p
    
    except:
        print("Title not found")


#Featured image
    image_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(image_url)

    browser.click_link_by_id("full_image")
    browser.click_link_by_partial_text("more info")
    image_html = browser.html
    image_soup = bs(image_html, 'html.parser')
    featured_image = image_soup.body.find("figure", class_="lede")

    # Define the Base URL
    base_url='https://www.jpl.nasa.gov'

    link = featured_image.find('a')
    href = link['href']

    # Combine both parts of the url to create the full url
    featured_image_url = base_url + href

    listings["featured_image_url"] = featured_image_url

#Mars Facts Table
    #URL to scrape:
    mars_facts_url = "https://space-facts.com/mars/"

    #Find the first table, and read into a dataframe
    facts_df = pd.read_html(mars_facts_url)[0]
    facts_df.columns = ["Description", "Value"]
    mars_facts_html = facts_df.to_html()
    listings["mars_facts_html"] = mars_facts_html

#Hemispheres
    #Define the starting point url
    hemispheres_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"

    #Create an empty list that will contain the browser htmls. These will be an ingredient in the "soup" later

    browser_htmls = []
    hemispheres = ['Cerberus', 'Schiaparelli', 'Syrtis', 'Valles']

    for x in hemispheres:
        browser.visit(hemispheres_url)
        browser.click_link_by_partial_text(x)
        browser.click_link_by_partial_text('Open')
        browser_htmls.append(browser.html)

    base_url = 'https://astrogeology.usgs.gov'
    img_url = []


    #SoupLoop for images
    for x in browser_htmls:
        soup = bs(x, 'html.parser')
        hemisphere = soup.body.find('img', class_ = 'wide-image')
        image = hemisphere['src']
        hemisphere_url = base_url + image
        img_url.append(hemisphere_url)

        hemisphere_image_urls = dict(zip(hemispheres, img_url))
        listings["hemisphere_image_urls"] = hemisphere_image_urls

    listings["img_url"] = img_url
    listings["hemispheres"] = hemispheres

    return listings
    
# End of scraping

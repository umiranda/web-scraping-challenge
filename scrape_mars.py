import requests
import json 
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup as bs
from splinter import Browser
import pandas as pd
import os
import time
import pymongo



def init_browser():
    executable_path = {'executable_path' : '/usr/local/bin/chromedriver'}
    return Browser('chrome', **executable_path, headless=False)

def scrape():
    browser = init_browser()
    mars_dict = {}

    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    html = browser.html 
    soup = bs(html, 'html.parser')
    #Finding the latest news title and assigning to a variable
    content = soup.find("div", class_='content_page')
    titles = content.find_all("div", class_='content_title')
    news_title = (titles[0].text.strip())
    news_title

    #Finding the latezt news Paragraph text and assigning to a variable
    article_text = content.find_all("div", class_='article_teaser_body')
    news_p = article_text[0].text
    news_p

    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)

    full_image = browser.find_by_id("full_image")
    full_image.click()
    
    more_info = browser.links.find_by_partial_text("more info")
    more_info.click()

    html = browser.html
    img_soup = bs(html, 'html.parser')

    img_path = img_soup.select_one('figure.lede a img').get("src")
    img_path

    featured_img_url = f"https://www.jpl.nasa.gov{img_path}"
    featured_img_url

    url_facts = 'https://space-facts.com/mars/'
    browser.visit(url_facts)
    html = browser.html
    soup = bs(html, 'html.parser')

    mars_facts_tables = pd.read_html(url_facts)
    df_facts_table = mars_facts_tables[0]
    df_facts_table.columns = ["Description", "Mars"]
    mars_html_table = df_facts_table.to_html()
    mars_html_table.replace('\n', '')

    url_facts = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url_facts)
    html = browser.html
    soup = bs(html, 'html.parser')
    large_photos = soup.find_all('div', class_='item')

    hemi_main_url = 'https://astrogeology.usgs.gov'

    #appending url string to a dictionary as well as the title
    hemi_ima_url = []

    for i in large_photos: 
   
        title = i.find('h3').text
        partial_img_url = i.find('a', class_='itemLink product-item')['href']
        browser.visit(hemi_main_url + partial_img_url) 
        partial_img_html = browser.html
        soup = bs( partial_img_html, 'html.parser')
        img_url = hemi_main_url + soup.find('img', class_='wide-image')['src']
        hemi_ima_url.append({"title" : title, "img_url" : img_url})
    
    hemi_ima_url

    mars_dict={
        "news_title_test": news_title,
        "news_p": news_p,
        "featured_img_url": featured_img_url,
        "fact_table": mars_html_table,
        "hemisphere_images": hemi_ima_url
    }
    return mars_dict





import pandas as pd
from splinter import Browser
from bs4 import BeautifulSoup


def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)


def scrape_info():

    browser = init_browser()

    # NASA Mars News
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    news_title = soup.find('div', class_='content_title').a.text
    news_p = soup.find('div', class_='article_teaser_body').text

    # JPL Mars Space Images - Featured Image
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    featured_image_url_base = soup.find('article', class_='carousel_item')[
        'style'].split("('", 1)[1].split("')")[0]
    link_split = url.split("/spaceimages")[0]
    featured_image_url = link_split + featured_image_url_base

    # Mars Weather
    url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    mars_weather = soup.find(
        'p', class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text").text.split("pic")[0]

    # Mars Facts
    url = 'https://space-facts.com/mars/'
    browser.visit(url)

    tables = pd.read_html(url)
    df = tables[0]
    df.columns = ['Attribute', 'Information']
    df.set_index('Attribute', inplace=True)
    html_table = df.to_html()

    # Mars Hemispheres
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    results = soup.find_all('div', class_='item')
    split_url = url.split("/search")[0]
    hemisphere_urls = []

    for result in results:
        browser.visit(split_url + result.a['href'])
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')
        title = soup.find('h2', class_='title').text
        img_result = soup.find('img', class_='wide-image')['src']
        img_url = split_url + img_result
        hemisphere_urls.append({'title': title, 'img_url': img_url})

    # Store all results in dictionary
    mars_data = {
        'news_title': news_title,
        'news_p': news_p,
        'featured_image_url': featured_image_url,
        'mars_weather': mars_weather,
        'html_table': html_table,
        'hemisphere_urls': hemisphere_urls
    }

    browser.quit()

    return mars_data

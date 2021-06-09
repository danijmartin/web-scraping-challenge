from splinter import Browser
from bs4 import BeautifulSoup as bs
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd

def scrape():
    # Setting up Splinter
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    # Connecting NASA Mars News url
    url = 'https://redplanetscience.com/'
    browser.visit(url)

    # Scraping page into Soup
    html = browser.html
    soup = bs(html, 'html.parser')

    # Grabbing first article name
    news_title = soup.find('div', class_='content_title').get_text()

    # Grabbing article paragraph
    news_p = soup.find('div', class_='article_teaser_body').get_text()

    # Connecting JPL Mars Space Images - Featured Image url
    url = 'https://spaceimages-mars.com/'
    browser.visit(url)

    # Using Splinter to grap featured image link
    featured_image_url = browser.find_by_tag("img[class='headerimage fade-in']")['src']

    url = 'https://galaxyfacts-mars.com/'

    # Using Pandas to read Mars Facts tables
    tables = pd.read_html(url)

    # Storing Mars facts table
    mars_facts_df = tables[1]

    # Converting table to html code
    html_table = mars_facts_df.to_html()

    # Removing new lines in html_table
    html_table.replace('\n', '')

    # Connecting Mars Hemispheres url
    url = 'https://marshemispheres.com/'
    browser.visit(url)

    links = []

    divs = browser.find_by_tag("div[class='item']")

    for div in divs:
        link = divs.find_by_tag('a')['href']
        links.append(link)

    hemisphere_image_urls = []

    for link in links:
        # Connecting url
        url = link
        browser.visit(url)
        # Scraping page into Soup
        html = browser.html
        soup = bs(html, 'html.parser')
        title = soup.find('h2', class_='title').get_text()
        url = browser.find_by_text('Original')['href']
        dictionary = {'title': title, 'img_url': url}
        hemisphere_image_urls.append(dictionary)

    browser.quit()

    # Storing Data in Dictionary

    mars_data = {
        'News_Title': news_title,
        'News_Paragraph': news_p,
        'Featured_Image': featured_image_url,
        'Table': html_table,
        'Hemisphere_Images': hemisphere_image_urls
    }

    # Returning results of Scrape
    return mars_data

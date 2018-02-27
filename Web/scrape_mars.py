def scrape():
    import pandas as pd
    from bs4 import BeautifulSoup as bs
    from splinter import Browser

    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    browser = Browser('chrome', **executable_path, headless=True)

    def give_me_soup(url):
        browser.visit(url)
        html = browser.html
        soup = bs(html, 'html.parser')
        return soup

    soup = give_me_soup('https://mars.nasa.gov/news/?page=0&per_page=15&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest')

    article_title = soup.find('div', class_='content_title').get_text().strip()
    article_summary = soup.find("div", class_="article_teaser_body").get_text().strip()

    soup = give_me_soup('https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars')

    imageloc = soup.find("article", class_="carousel_item")

    endurl = imageloc['style'][24:75]
    begurl = 'https://www.jpl.nasa.gov/'
    imgurl = begurl + endurl

    soup = give_me_soup('https://twitter.com/marswxreport?lang=en')

    tweet = soup.find("p", class_="tweet-text").get_text().strip()

    soup = give_me_soup('https://space-facts.com/mars/')

    table_tag = soup.find('table', class_='tablepress tablepress-id-mars')

    df = pd.read_html(str(table_tag))[0]

    html_output = df.to_html(index=False, header=False).replace('\n', '')

    def mars_imgurl_gen(url):
        soup = give_me_soup(url)
        image_tag = soup.find('img', class_='wide-image')
        base_url = 'https://astrogeology.usgs.gov'
        high_res_path = image_tag['src']
        image_url = base_url + high_res_path
        return image_url

    cerberus = mars_imgurl_gen('https://astrogeology.usgs.gov/search/map/Mars/Viking/cerberus_enhanced')
    schiaparelli = mars_imgurl_gen('https://astrogeology.usgs.gov/search/map/Mars/Viking/schiaparelli_enhanced')
    syrtis_major = mars_imgurl_gen('https://astrogeology.usgs.gov/search/map/Mars/Viking/syrtis_major_enhanced')
    valles_marineris = mars_imgurl_gen('https://astrogeology.usgs.gov/search/map/Mars/Viking/valles_marineris_enhanced')

    hemisphere_image_urls = [
    {"title": "Valles Marineris Hemisphere", "img_url": valles_marineris},
    {"title": "Cerberus Hemisphere", "img_url": cerberus},
    {"title": "Schiaparelli Hemisphere", "img_url": schiaparelli},
    {"title": "Syrtis Major Hemisphere", "img_url": syrtis_major}
    ]

    output = {'article_title': article_title,
          'article_summary': article_summary,
          'feature_image_url': imgurl,
          'tweet': tweet,
          'table_html': html_output,
          'hemisphere_list': hemisphere_image_urls}

    return output

from scrapy.spiders import BaseSpider
from scrapy.selector import HtmlXPathSelector
from scrapy.http import Request

from zillow_scraper.items import ZillowScraperItem

import re

def lowercase(string):
    string = string.lower().strip()
    return re.sub(r'\s+', '_', string)

class TestSpider(BaseSpider):
    name = "zillowspider"
    allowed_domains = ["zillow.com"]
    start_urls = [
            "http://www.zillow.com/homes/for_sale/california_rb/",
    ]

    # override parse method
    def parse(self, response):
        hxs = HtmlXPathSelector(response)

        # extract the links for detail page
        links = hxs.xpath("//a[contains(@class,'hdp-link routable')]/@href").extract()
        for link in links:
            full_url = "http://zillow.com" + link
            
            # create new request for details page
            yield Request(full_url, callback=self.parse_home, meta={'url' : full_url})

            url = response.urljoin(response.xpath("//a[contains(.//text(), \'Next\')]/@href").extract_first())
            # create new request for next page
            yield Request(url, callback=self.parse)

    # callback for parsing details page
    def parse_home(self, response):
        hxs = HtmlXPathSelector(response)
        item = ZillowScraperItem()

        item['url'] = response.meta['url']

        # extract locations 
        city_state_code = response.xpath("//header[@class='zsg-content-header addr']/h1/span/text()").extract_first().split(",")
        state_code = city_state_code[1].strip().split(" ")
        item['address'] = response.xpath("//header[@class='zsg-content-header addr']/h1/text()").extract_first().strip()[:-1]
        item['city'] = city_state_code[0].strip()
        item['state'] = state_code[0].strip()
        item['zip_code'] = state_code[1].strip()

        # extract accomodations
        accomodations = response.xpath("//header[@class='zsg-content-header addr']/h3/span[@class='addr_bbs']/text()").extract()
        item['beds'] = ''.join(re.findall(r'\d+', accomodations[0]))
        item['baths'] = ''.join(re.findall(r'\d+', accomodations[1]))
        item['sq_ft'] = ''.join(re.findall(r'\d+', accomodations[2]))

        # extract price
        item['price'] = response.xpath("//div[contains(@class, 'main-row')]/span/text()").extract_first().strip()

        # extract the facts, features, etc using the list of selectors
        selectors = response.xpath("//div[contains(@class,'fact-group-container')]")
        for sel in selectors:
            # get header title
            title = sel.xpath("./h3/text()").extract_first()
            try:
                item[lowercase(title)] = [ fact for fact in sel.xpath(".//li/text()").extract() ]
            except KeyError:
                continue

        # extract county website
        cw = response.xpath("//a[contains(.//text(), \'County website\')]/@href").extract_first() 
        item['county_website'] = cw if cw is not None else ''

        # extract agent names
        agent_divs = response.xpath("//div[contains(@class, 'recipients')]")
        names = agent_divs[0].xpath(".//a[@class='profile-name-link']/text()").extract()
        phones = agent_divs[0].xpath(".//span[@class='snl phone']/text()").extract()
        item['agents'] = [ {'name' : name, 'phone' : phones[index]} for index, name in enumerate(names) ] if names and phones else []

        yield item






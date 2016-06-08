from scrapy.spiders import BaseSpider
from scrapy.selector import HtmlXPathSelector
from scrapy.http import Request

from zillow_scraper.items import ZillowScraperItem

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
        for index, link in enumerate(links):
            full_url = "http://zillow.com" + link
            
            # create new request for details page
            yield Request(full_url, callback=self.parse_home, meta={'count' : index})

            url = response.urljoin(response.xpath("//a[contains(.//text(), \'Next\')]/@href").extract_first())
            # create new request for next page
            yield Request(url, callback=self.parse)

    # callback for parsing details page
    def parse_home(self, response):
        hxs = HtmlXPathSelector(response)
        item = ZillowScraperItem()
        item['location'] = response.xpath("//header[@class='zsg-content-header addr']/h1/text()").extract_first().strip()[:-1]
        yield item


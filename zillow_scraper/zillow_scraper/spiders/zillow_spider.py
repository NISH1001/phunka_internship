from scrapy.spiders import BaseSpider, CrawlSpider, Rule
from scrapy.selector import HtmlXPathSelector
from scrapy.linkextractors import LinkExtractor

from scrapy.http import Request

from zillow_scraper.items import ZillowScraperItem

class ZillowSpider(CrawlSpider):
    name = "zillow"
    allowed_domains = ["zillow.com"]
    start_urls = [
            "http://www.zillow.com/homes/for_sale/california_rb/"
    ] 
    
    rules = [
        Rule(LinkExtractor(
                allow = (),
                restrict_xpaths = ("//a[contains(.//text(), \'Next\')]",),
            ),
            callback = 'parse_item',
            follow=True)
    ]
    
    def parse_item(self, response):
        # create a htmlxpathselector instance 
        hxs = HtmlXPathSelector(response)

        # select all links with this property -> gives those list of houses for sale
        links = hxs.xpath("//a[contains(@class,'hdp-link routable')]/@href").extract()

        for link in links:
            item = ZillowScraperItem()
            ret = "http://zillow.com" + link
            item['link'] = ret
            yield item

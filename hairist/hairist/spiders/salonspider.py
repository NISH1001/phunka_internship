from scrapy.spiders import BaseSpider
from scrapy.selector import Selector
from scrapy.http import Request

import re

from hairist.items import HairistItem

class SalonSpider(BaseSpider):
    name = "salonspider"
    allowed_domains = ["hairist.com"]
    start_urls = [
            ]

    def __init__(self):
        self.start = 1
        self.end = 2203
        self.url = "https://www.hairist.com.tr/index.php?page=salonDetay&salonID={}",

    def start_requests(self):
        print("-" * 50, "inside start_requests")

        requests = [
                        Request(
                            url = self.url.format(idx),
                            callback=self.parse,
                        )

                        for idx in range(self.start, self.end+1)
                ]
        return requests

    def parse(self, response):
        selector = Selector(response)
        print("-"*30)
        latlng = response.xpath("//div[@class='google-maps-link']/a/@href").extract()
        table = response.xpath("//table[@class='salondetay']")[0]
        tds = table.xpath(".//tr/td[3]")
        print(response.url)

        item = HairistItem()
        item['yetkili']                 = tds[0].xpath("./text()").extract_first().strip()
        item['kuafor_salonu_turu']      = tds[1].xpath("./text()").extract_first().strip()
        item['calisma_saatleri']        = tds[2].xpath("./text()").extract_first().strip()
        item['tatil_gunleri']           = tds[3].xpath("./text()").extract_first().strip()
        item['koltuk_sayisi']           = tds[4].xpath("./text()").extract_first().strip()
        item['kullanilan_markalar']     = tds[5].xpath(".//span/text()").extract()
        item['telfon']                  = tds[6].xpath("./text()").extract_first().strip()
        item['mobil']                   = tds[7].xpath("./text()").extract_first().strip()
        item['adres']                   = tds[8].xpath("./text()").extract_first().strip()
        item['ilce_il']                 = tds[9].xpath("./text()").extract_first().strip()
        item['email']                   = tds[10].xpath(".//a/text()").extract_first()

        image_urls = response.xpath("//ul[@class='gallery']//img/@src").extract()[1:]
        for index, url in enumerate(image_urls):
            image_urls[index] = re.sub(r"type=\d+","type=6", url)
        item['image_urls'] = image_urls

        yield item
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
        self.start = 2190
        self.end = 2203
        self.url = "https://www.hairist.com.tr/index.php?page=salonDetay&salonID={}"

    def start_requests(self):
        print("-" * 50, "inside start_requests")

        requests = [
                        Request(
                            url = self.url.format(idx),
                            callback=self.parse,
                            meta = { 'id' : idx },
                        )

                        for idx in range(self.start, self.end+1)
                ]
        return requests

    def parse(self, response):
        selector = Selector(response)
        item = HairistItem()
        try:
            #latlng = response.xpath("//div[@class='google-maps-link']")
            table = response.xpath("//table[@class='salondetay']")[0]
            tds = table.xpath(".//tr/td[3]")

            item['id'] = response.meta['id']
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
            item['image_local_path'] = ''

            image_urls = response.xpath("//ul[@class='gallery']//img/@src").extract()[1:]
            for index, url in enumerate(image_urls):
                image_urls[index] = re.sub(r"type=\d+","type=6", url)
            item['image_urls'] = image_urls

            iframe = response.xpath("//iframe/@src")[0].extract()
            found = re.search(r"2d(.*)!3d(\d+\.\d+)!", iframe)
            latlng = [ found.group(1), found.group(2)]
            item['latlng'] = latlng

        except:
            return
        yield item





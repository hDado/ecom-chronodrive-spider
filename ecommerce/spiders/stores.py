import scrapy
from scrapy import Request


class StoresSpider(scrapy.Spider):
    # scrapper name
    name = "stores"
    # base_url

    base_url = "https://www.chronodrive.com/magasins-chronodrive"
    orig_url = "https://www.chronodrive.com"

    def start_requests(self):
        yield Request(url=self.base_url, callback=self.next_move)

    def next_move(self, response):
        st_links = response.xpath("//a[@class='drive-link']")
        for link in st_links:
            stores_f = self.orig_url + link.xpath("./@href").get()

            yield Request(url=stores_f, callback=self.landing_page)

    def landing_page(self, response):
        info_gen = response.xpath("//div[@class='left']")
        for info in info_gen:
            yield {
                "street_adresse": info.xpath(".//div/p/span/span[1]/text()").get(),
                "postal_code": info.xpath(".//div/p/span/span[2]/text()").get(),
                "departement_name": info.xpath(".//div/p/span/span[3]/text()").get(),
                "telephone": info.xpath(
                    ".//div[contains(@class,'mag-info')][2]/p/strong/span/text()"
                ).get(),
                "id": info.xpath(".//div[@class='map-bloc hidden']/@id").get()[-4:],
            }

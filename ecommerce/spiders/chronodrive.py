import scrapy
from scrapy import Request
from scrapy.shell import inspect_response
import json
import pandas as pd 
from ecommerce.items import EcommerceItem


class ChronodriveSpider(scrapy.Spider):
    # scrapper name
    name = "chronodrive"
    # base_url

    base_url = "https://www.chronodrive.com"

    def start_requests(self):
        dt = pd.read_csv("./chrono_data.csv")
        id_s= set(dt["id"])
        id = list(id_s)
        for i in id:
            yield Request(url=self.base_url, cookies={"chronoShop": f"shopId={i}"}, callback=self.next_move)

    def next_move(self, response):
        rayons = response.xpath("(//ul[@class='footer-seo-links-list'])[1]/li/a")
        for sub in rayons:
            rayon_link = self.base_url + sub.xpath(".//@href").get()
            rayon_name = sub.xpath(".//text()").get()
            yield Request(url=rayon_link, callback=self.parse_sub_category)

    def parse_sub_category(self, response):
        
        sub_category = response.xpath("//div[@class='navSeoStageOne-item']/a")
        for link in sub_category:
            sub_link_f = self.base_url + link.xpath(".//@href").get()
            yield Request(url=sub_link_f, callback=self.parse_products)

    def parse_products(self, response):
        # inspect_response(response, self)
        item = EcommerceItem()
        for product in response.xpath("//div[@id='productListZone']/article"):
            d = product.xpath(".//span[@class='item-goodPrice']//text()").getall()
            price = ''.join([i.strip() for i in d]) if d else None
            item["product_description"] = product.xpath(".//div[@class='item-desc']/text()").get()
            item["quantity_weight"] = product.xpath(".//span[@class='item-qtyCapacity']/text()").get()
            item["price"] = price
            item["product_link"] = self.base_url + product.xpath(".//a[contains(@data-rel,'lap_grp')]/@href").get()

            yield item
    


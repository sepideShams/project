# -*- coding: utf-8 -*-
import scrapy
from scrapy.selector import Selector
from Data_scrapper.items import EqItem


class IrscSpider(scrapy.Spider):
    name = "irsc"
    allowed_domains = ["irsc.ut.ac.ir"]
    start_urls = (
        'http://irsc.ut.ac.ir/',
    )

    def parse(self, response):
        for data in Selector(response).xpath(".//*[@id='AutoNumber3']"):
            item = EqItem()
            item['Origin_Time'] = data.xpath('.//a//font//b//text()').extract()
            item['Magnitude'] = data.xpath('.//tr//td[2]//b//text()').extract() or None
            item['Latitude'] = data.xpath(".//table//tr[contains(@class, 'DataRow')]//td[3]//text()").extract()
            item['Longitude'] = data.xpath(".//table//tr[contains(@class, 'DataRow')]//td[4]//text()").extract()
            item['Depth'] = data.xpath(".//table//tr[contains(@class, 'DataRow')]//td[5]//text()").extract()
            item['Region'] = data.xpath(".//table//tr[contains(@class, 'DataRow')]//td[6]//text()").extract()
            for o, m, la, lo, d, r in zip(item['Origin_Time'], item['Magnitude'], item['Latitude'], item['Longitude'], item['Depth'], item['Region']):
                item = EqItem(Origin_Time=o, Magnitude=m, Latitude=la, Longitude=lo, Depth=d, Region=r)
                yield item
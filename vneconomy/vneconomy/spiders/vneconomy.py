from pathlib import Path

import scrapy

from ..items import VneconomyItem

class QuotesSpider(scrapy.Spider):
    name = "vneconomy"

    def start_requests(self):
        urls = [
            "https://vneconomy.vn/vang-hoi-gia-sau-9-phien-giam-lien-tiep-trien-vong-van-am-dam.htm",
        ]

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        page = response.url.split("/")[-2]
        title = response.url.split("/")[-2] + "_" +response.url.split("/")[-1]
        text = response.selector.css('.detail__content ::text').getall()
        item = VneconomyItem()
        for each_text in text:
            item['text'] = each_text
            yield item

        graph_img = None
        for img in response.css("img"):
            if 'data-original' in img.attrib.keys():
                graph_img = img.attrib['data-original']
        filename = f"{title}.html"
        Path(filename).write_bytes(response.body)
        self.log(f"Saved file {filename}")
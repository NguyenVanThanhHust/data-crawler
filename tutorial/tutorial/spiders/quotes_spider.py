from pathlib import Path

import scrapy

from ..items import TutorialItem  

class QuotesSpider(scrapy.Spider):
    name = "quotes"

    def start_requests(self):
        urls = [
            "https://quotes.toscrape.com/page/1/",
            # "https://quotes.toscrape.com/page/3/",
        ]

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        # creating items dictionary 
        items = TutorialItem()    
        Quotes_all = response.xpath('//div/div/div/span[1]')
 
        # These paths are based on the selectors
         
        for quote in Quotes_all:    #extracting data
            items['Quote'] = quote.css('p::text').extract()
            yield items

        author_page_links = response.css(".author + a")
        yield from response.follow_all(author_page_links, self.parse_author)

        pagination_links = response.css("li.next a")
        yield from response.follow_all(pagination_links, self.parse)

    def parse_author(self, response):
        def extract_with_css(query):
            return response.css(query).get(default="").strip()

        yield {
            "name": extract_with_css("h3.author-title::text"),
            "birthdate": extract_with_css(".author-born-date::text"),
            "bio": extract_with_css(".author-description::text"),
        }
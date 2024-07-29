import scrapy
from scrapy.loader import ItemLoader
from tutorial.items import QuoteItem


class QuotesSpider (scrapy.Spider):
    name = "quotes"
    allowed_domains = ["toscrape.com"]
    start_urls = ['http://quotes.toscrape.com']

    def parse(self, response):
        self.logger.info('This is my first Spider.')

        # quotes = response.css('div.quote')
        quotes = response.xpath("//div[@class='quote']")

        for quote in quotes:
            loader = ItemLoader(item=QuoteItem(), selector=quote)

            # loader.add_css('quote_content', '.text::text')
            loader.add_xpath('quote_content', '//*[@class="text"]/text()')

            # loader.add_css('tags', '.tags > a::text')
            loader.add_xpath('tags', './/*[@class="tags"]//a/text()')

            quote_item = loader.load_item()

            # author_url = quote.css('.author + a::attr(href)').get()
            author_url = quote.xpath("//*[@class='quote']//a/@href").get()

            yield response.follow(
                author_url, self.parse_author, meta={'quote_item': quote_item}
            )

        # next_page = response.css('li.next a::attr(href)').get()
        next_page = response.xpath('//li[@class="next"]//a/@href').get()

        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)

    def parse_author(self, response):
        quote_item = response.meta['quote_item']
        loader = ItemLoader(item=quote_item, response=response)

        # loader.add_css('author_name', '.author-title::text')
        loader.add_xpath(
            'author_name', '//*[@class="author-title"]/text()'
        )

        # loader.add_css('author_birthday', '.author-born-date::text')
        loader.add_xpath(
            'author_birthday',
            '//*[@class="author-born-date"]/text()'
        )

        # loader.add_css('author_bornlocation', '.author-born-location::text')
        loader.add_xpath(
            'author_bornlocation',
            '//*[@class="author-born-location"]/text()'
        )

        # loader.add_css('author_bio', '.author-description::text')
        loader.add_xpath(
            'author_bio',
            '//*[@class="author-description"]/text()'
        )

        yield loader.load_item()

# import scrapy
#
#
# class QuotesSpider(scrapy.Spider):
#     name = "quotes"
#     start_urls = [
#         'http://quotes.toscrape.com/tag/humor/',
#     ]
#
#     def parse(self, response):
#         for quote in response.css('div.quote'):
#             yield {
#                 'text': quote.css('span.text::text').extract_first(),
#                 'author': quote.xpath('span/small/text()').extract_first(),
#             }
#
#         next_page = response.css('li.next a::attr("href")').extract_first()
#         if next_page is not None:
#             yield response.follow(next_page, self.parse)
#
#
# class AuthorSpider(scrapy.Spider):
#     name = 'author'
#
#     start_urls = ['http://quotes.toscrape.com/']
#
#     def parse(self, response):
#         # follow links to author pages
#         for href in response.css('.author + a::attr(href)'):
#             yield response.follow(href, self.parse_author)
#
#         # follow pagination links
#         for href in response.css('li.next a::attr(href)'):
#             yield response.follow(href, self.parse)
#
#     def parse_author(self, response):
#         def extract_with_css(query):
#             return response.css(query).extract_first().strip()
#
#         yield {
#             'name': extract_with_css('h3.author-title::text'),
#             'birthdate': extract_with_css('.author-born-date::text'),
#             'bio': extract_with_css('.author-description::text'),
#         }

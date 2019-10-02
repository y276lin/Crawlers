import scrapy
import re

class WallstreetSpider(scrapy.Spider):

    name = "question_url"
    start_urls = [
            'https://www.wallstreetoasis.com/forum/investment-banking',
        ]

    for i in range(1, 607):
        start_urls.append('https://www.wallstreetoasis.com/forum/investment-banking?page=' + str(i))
    
    # print(start_urls)

    def parse(self, response):

        for question in response.css("td.title"):
            question_title = question.css("span::text").get()
            question_url = question.css("a::attr(href)").get()

            if question_title is not None:
                yield{
                    "question"  : question.css("span::text").extract(),
                    "url" : response.urljoin(question_url)
                }

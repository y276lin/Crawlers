import scrapy
import re

class WallstreetSpider(scrapy.Spider):

    name = "question_url"
    start_urls = [
            'https://insurance-forums.com/community/forums/auto-insurance-forum.38/',
        ]

    for i in range(2, 63):
        start_urls.append('https://insurance-forums.com/community/forums/auto-insurance-forum.38/page-' + str(i))
    
    print(start_urls)

    def parse(self, response):

        for question in response.css("h3.title"):
            question_title = question.css("a::text").get()
            question_url = question.css("a::attr(href)").get()

            if question_title is not None:
                yield{
                    "question"  : question.css("a::text").extract(),
                    "url" : response.urljoin(question_url),
                    
                }
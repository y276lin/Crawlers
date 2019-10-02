import scrapy
import re

class CitydataSpider(scrapy.Spider):

    name = "question_url"
    start_urls = [
            'http://www.city-data.com/forum/economics/',
        ]
    # for i in range(2, 154):
    #     start_urls.append('http://www.city-data.com/forum/economics/index' + str(i) + '.html')
    
    #print(start_urls)
    # title_id = 'thread_title_' + r'^[0-9]+$'
    # m = re.match(title_id, "thread_title_328061")
    title_id =  r'^[0-9]+$'
    # m = re.match(title_id, "328061")
    # print(m.group(0))
    # print(type(title_id))



    def parse(self, response):
        
        tbody = response.css("tbdoy")

        for question in response.css("a#thread_title_" + str(r'[0-9]+$')):
            question_title = question.css("a::text").get()
            question_url = question.css("a::attr(href)").get()

            if question_title is not None:
                yield{
                    "question"  : question.css("a::text").extract(),
                    "url" : response.urljoin(question_url)
                }
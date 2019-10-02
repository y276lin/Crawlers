import scrapy
import json


class WallstreetQuestionsSpider(scrapy.Spider):

    name = "related_questions"
    start_urls = []

    with open('url.json')as json_file:
        question_and_url = json.load(json_file)
        for item in question_and_url:
            start_urls.append(item['url'])
        # print(start_urls)

    def parse(self, response):

        question = response.css("h1::text").extract()
        related_list = response.css("div.content-block__text-wrapper")
        related_questions = related_list.css("a::text").extract()
        
        yield{
            "question"  : question,
            "related_questions" : related_questions
        }
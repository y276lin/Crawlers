import re
import json
import sys
import time
import random
import os
from scrapy import Request
from scrapy.spiders import Spider
from scrapyspider.items import VCMtimesMovieItem


class MtimesMovieContentSpider(Spider):
  name = 'Mtimes_Movie_Contents'
  path = os.path.split(os.path.abspath(__file__))[0]
  time_stamp = time.strftime("%Y%m%d", time.localtime())
  headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36',
  }
  custom_settings = {
    'FEED_EXPORT_ENCODING': 'utf-8',
    'FEED_FORMAT': 'json',
    'FEED_URI': path+'/theater_movie_contents_'+time_stamp+'.json',
  }


  def start_requests(self):
    with open(self.path+'/theater_movie_urls_new.json', mode='r') as url_json:
      url_dict =json.load(url_json)
    for url in url_dict:
      item = VCMtimesMovieItem()
      item['movie_url'] = url['movie_url']
      yield Request(url['movie_url'], headers=self.headers, meta={'item_l1':item}, callback=self.parse_movie_mainpagecontent, priority=0)

  def __init__(self):
    reload(sys)
    sys.setdefaultencoding("utf-8")

  def parse_movie_mainpagecontent(self, response):
    item = response.meta['item_l1']
    item['movie_name'] = response.xpath(
      '//div[@class="db_head"]/div[1]/h1/text()').extract()
    item['director'] = response.xpath(
      u'//dl[@class="info_l"]//strong[contains(text(),"director")]/../a/text()').extract()
    item['movie_ontime'] = response.xpath(
      '//div[@class="otherbox __r_c_"]/a[@property="v:initialReleaseDate"]/text()').extract()
    item['movie_duration'] = response.xpath(
      '//div[@class="otherbox __r_c_"]/span/text()').extract()
    item['movie_style'] = response.xpath(
      '//div[@class="otherbox __r_c_"]/a[@property="v:genre"]/text()').extract()
    item['movie_region'] = response.xpath(
      u'//dl[@class="info_l"]//strong[contains(text(),"Country&Region")]/../a/text()').extract()
    item['movie_type'] = list(["Movies"])
    item['movie_alias'] = response.xpath(
      u'//dl[@class="info_l"]//strong[contains(text(),"more")]/../span/text()').extract()
    yield Request(response.request.url + 'fullcredits.html', headers=self.headers,
                  meta={'item_l2': item, 'dont_redirect': True,
                        'handle_httpstatus_list': [302]}, callback=self.parse_movie_actors, priority=1)

  def parse_movie_actors(self, response):
    item = response.meta['item_l2']
    actors = response.xpath(
      '//div[@class="db_actor"]//dd/div[@class="actor_tit"]/div[1]/h3/a/text()').extract()
    if len(actors) > 8:
      item['actor'] = actors[0:8]
    else:
      item['actor'] = actors
    roles = response.xpath(
      '//div[@class="db_actor"]//dd/div[@class="character_tit"]/div[1]//h3/text()').extract()
    if len(roles) > 8:
      item['role'] = roles[0:8]
    else:
      item['role'] = roles
    yield Request(response.request.url.replace('fullcredits', 'awards'), headers=self.headers,
                  meta={'item_l3': item, 'dont_redirect': True,
                        'handle_httpstatus_list': [302]}, callback=self.parse_movie_award, priority=2)

  def parse_movie_award(self, response):
    try:
      item = response.meta['item_l3']
      item['movie_award_num'] = response.xpath(
        u'//div[@id="awardInfo_data"]//h3[text()=" Award："]/strong[1]/text()').extract()
      item['movie_subaward_nominate'] = response.xpath(
        u'//div[@id="awardInfo_data"]//dt[text()="Award"]/../dd/span/text()').extract()
      item['movie_award'] = response.xpath(
        u'//div[@id="awardInfo_data"]//dt[text()="Award"]/../preceding-sibling::*[1]/b/text()').extract()
      item['movie_awardyear'] = response.xpath(
        u'//div[@id="awardInfo_data"]//dt[text()="Award"]/../preceding-sibling::*[1]/span/a/text()').extract()
    except Exception:
      pass
    finally:
      yield Request(response.request.url.replace('awards', 'details'), headers=self.headers,
                    meta={'item_l4': item, 'dont_redirect': True,
                          'handle_httpstatus_list': [302]}, callback=self.parse_movie_others, priority=3)

  def parse_movie_others(self, response):
    item = response.meta['item_l4']
    item['movie_language'] = response.xpath(
      u'//div[@class="db_movieother_2"]//strong[contains(text(),"Subs")]/../p/a/text()').extract()
    movieid = filter(str.isdigit, response.request.url)
    t = self.time_generator()
    url_score = 'http://service.library.mtime.com/Movie.api?Ajax_CallBack=true&Ajax_CallBackType=Mtime.Library.Services&Ajax_CallBackMethod=GetMovieOverviewRating&Ajax_CrossDomain=1&Ajax_RequestUrl=http%3A%2F%2Fmovie.mtime.com%2F' + movieid + '%2F&t=' + t + '&Ajax_CallBackArgument0=' + movieid
    yield Request(url_score, headers=self.headers, meta={'item_l5': item, 'dont_redirect': True,
                                                         'handle_httpstatus_list': [302]},
                  callback=self.parse_movie_score, priority=4)

  def parse_movie_score(self, response):
    item = response.meta['item_l5']
    html = response.text
    parttern = re.compile(r'"RatingFinal":\d,|"RatingFinal":\d+\.\d,')
    scores = parttern.findall(html)
    if len(scores) > 0:
      score = parttern.findall(html)[0]
      item['Movie_score'] = score[14:-1]
    yield item

  def time_generator(self):
    num = random.randint(1000, 9999)
    t = time.strftime('%Y%m%d%H%M%S' + str(num), time.localtime())
    return t






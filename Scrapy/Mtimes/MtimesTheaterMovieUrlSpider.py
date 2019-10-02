
import re
import sys
import os
from scrapy import Request
from scrapy.spiders import Spider
from scrapyspider.items import VCMtimesMovieurlItem

class MtimesTheaterMovieUrlSpider(Spider):
    name = 'Theater_Movie_urls'
    path = os.path.split(os.path.abspath(__file__))[0]
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'
    }
    custom_settings = {
        'FEED_EXPORT_ENCODING': 'utf-8',
        'FEED_FORMAT': 'json',
        'FEED_URI':  path+'/theater_movie_urls_new.json',
    }
    # handle_httpstatus_list = [404]
    def __init__(self):
      reload(sys)
      sys.setdefaultencoding("utf-8")



    def start_requests(self):
      # t = self.time_generator()
      # url = 'http://service.channel.mtime.com/service/search.mcs?Ajax_CallBack=true&Ajax_CallBackType=Mtime.Channel.Pages.SearchService&Ajax_CallBackMethod=SearchMovieByCategory&Ajax_CrossDomain=1&Ajax_RequestUrl=http%3A%2F%2Fmovie.mtime.com%2Fmovie%2Fsearch%2Fsection%2F%3Fyear%3D2017%23pageIndex%3D1%26year%3D2017&t=' + t + '&Ajax_CallBackArgument0=&Ajax_CallBackArgument1=0&Ajax_CallBackArgument2=0&Ajax_CallBackArgument3=0&Ajax_CallBackArgument4=0&Ajax_CallBackArgument5=0&Ajax_CallBackArgument6=0&Ajax_CallBackArgument7=0&Ajax_CallBackArgument8=&Ajax_CallBackArgument9=2017&Ajax_CallBackArgument10=2017&Ajax_CallBackArgument11=0&Ajax_CallBackArgument12=0&Ajax_CallBackArgument13=0&Ajax_CallBackArgument14=1&Ajax_CallBackArgument15=0&Ajax_CallBackArgument16=1&Ajax_CallBackArgument17=4&Ajax_CallBackArgument18=1&Ajax_CallBackArgument19=0'
      url ='http://theater.mtime.com/China_Beijing/#'
      yield Request(url=url, headers=self.headers, callback=self.parse, dont_filter=True)

    def parse(self, response):
      html = response.xpath(
      '//div[@id="hotplayContent"]/div[1]').extract()[0]
      parttern = re.compile(r'http://movie.mtime.com/\d+/')
      links = parttern.findall(html)
      movie_ids = list(set(links))
      movie_ids.sort(key=links.index)
      for link in movie_ids:
        item = VCMtimesMovieurlItem()
        item['movie_url'] = link
        yield item
          # item['movie_url'] = movie_url
          #yield Request(movie_url, headers=self.headers, meta={'item_l1':item}, callback=self.parse_movie_mainpagecontent)
          
        # if int(page_num) < 200:
        #   page_num = 'pageIndex=' + str(int(page_num)+1)
        #   next_url = re.sub(r'pageIndex=\d+', page_num, response.url)
        #   request = Request(url=next_url, callback=self.parse, dont_filter=True, priority=0)
        #   request.meta['PhantomJS'] = True
        #   print "Crawling" + page_num
        #   yield request
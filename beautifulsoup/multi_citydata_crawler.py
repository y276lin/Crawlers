import requests, sys
import re
from bs4 import BeautifulSoup


if __name__ == "__main__":
     target = 'http://www.city-data.com/forum/personal-finance/'
     req = requests.get(url = target)
     soup = BeautifulSoup(req.content, 'html.parser')
     ids = "".join(['thread_title_',r'[0-9]+'])
     # print(type(ids))
     post_list = soup.find_all('a', id = "".join(['thread_title_',r'[0-9]+']))
     print(post_list)
     test = soup.find_all('a', id = "thread_title_3086630")
     print(test)

     m = re.match(ids, "thread_title_3086630")
     print(m.group())
         
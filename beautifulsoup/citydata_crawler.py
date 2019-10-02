import requests, sys
from bs4 import BeautifulSoup

f = open("citydata_output.txt", "w+")

if __name__ == "__main__":
     target = 'http://www.city-data.com/forum/personal-finance/3085807-better-pay-extra-mortgage-pool-loan.html'
     req = requests.get(url = target)
     soup = BeautifulSoup(req.content, 'html.parser')
     question = soup.find('strong').text
     f.write("Question: " + question + "\n\n")
     f.write("Related Questions: " + "\n\n")
     related_list = soup.find_all('a', attrs={"onclick": "_gaq.push(['_trackEvent','forum_similarthread','click']);"})
     for related in related_list:
         related = related.text + "\n"
         f.write(related)

     f.close()

import requests, sys
from bs4 import BeautifulSoup

f = open("wallstreet_output.txt", "w+")

if __name__ == "__main__":
     target = 'https://www.wallstreetoasis.com/forums/new-jp-morgan-sa-2020-thread'
     req = requests.get(url = target)
     html = req.text
     soup = BeautifulSoup(html)
     question = soup.find("h1", class_ = "m-t-md m-r-sm wso-forum-title").text
     f.write("Question: " + question + "\n\n")
     f.write("Related Questions: " + "\n\n")
     related_list = soup.find_all('a', class_ = 'content-block__text content-block__link')
     for related in related_list:
         related = related.text + "\n"
         f.write(related)
         
     f.close()
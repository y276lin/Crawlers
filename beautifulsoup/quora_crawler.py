import requests, sys
from bs4 import BeautifulSoup

f = open("quora_output.txt", "w+")

if __name__ == "__main__":
     target = 'https://www.quora.com/What-was-the-biggest-financial-mistake-you-made-that-you-still-regret-to-this-day'
     req = requests.get(url = target)
     html = req.text
     soup = BeautifulSoup(html)
     question_loc = soup.find('span', class_ = 'ui_qtext_rendered_qtext')
     question = question_loc.text
     f.write("Question: " + question + "\n\n")
     f.write("Related Questions: " + "\n\n")
     related_list = soup.find_all('a', class_='question_link')
     for related in related_list:
         related = str(related.get('href') + "\n")
         output = related.replace("-", " ")
         f.write(output[1:])
     f.close()
    
import bs4
import requests
import re


url = 'https://www.qiushibaike.com/text/page/'
parser = 'html5lib'


def getJokes(page, item_index):
    html = requests.get(url+str(page)).text
    bsObj = bs4.BeautifulSoup(html, parser)
    jokesDiv = bsObj.find_all('div', {'id': re.compile('qiushi_tag_*')})
    print(len(jokesDiv))
    index = item_index if int(item_index) < len(jokesDiv) else int(item_index) % len(jokesDiv)
    return jokesDiv[index].find('span').get_text()


# print(getJokes(13,3))



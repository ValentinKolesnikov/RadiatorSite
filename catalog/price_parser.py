from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import re
import requests


def get_price():
    user_agent = UserAgent()
    headers = {"User-Agent": user_agent.random}
    base_url = 'https://catalog.onliner.by/radiators'



    response = requests.get('https://belsklad.by/otoplenie-i-vodosnabzhenie/radiatory-otoplenija', headers)
    print(response.text)
    f = open('text.html', 'w', encoding='utf-8')
    f.write(response.text)
    f.close()
    soup = BeautifulSoup(response.text, 'lxml')
    tds = soup.findAll('span', 'us-module-price-actual')
    print(tds)
    radiator = {'manufacturer': 'Royal Thermo',
                'height': 300,
                'depth': 80}


    # tds = soup.findAll(id=re.compile('RAL_'))
    # names = [td['id'].replace('_', ' ') for td in tds]400
    # bgs = ["#" + td['bgcolor'] for td in tds]
    # colors = []
    # for i, y in zip(names, bgs):
    #     colors.append({"name": i, "color": y})
    # return colors

var = get_price()
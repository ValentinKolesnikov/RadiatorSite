from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import re
import requests


def get_colors():
    user_agent = UserAgent()
    headers = {"User-Agent": user_agent.random}
    response = requests.get('https://catalog.onliner.by/', headers)
    soup = BeautifulSoup(response.text, 'lxml')
    radiator = {'manufacturer': 'Royal Thermo',
                'height': 300,
                'depth': 80}


    # tds = soup.findAll(id=re.compile('RAL_'))
    # names = [td['id'].replace('_', ' ') for td in tds]
    # bgs = ["#" + td['bgcolor'] for td in tds]
    # colors = []
    # for i, y in zip(names, bgs):
    #     colors.append({"name": i, "color": y})
    # return colors

var = get_colors()
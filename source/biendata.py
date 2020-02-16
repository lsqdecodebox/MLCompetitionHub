from datetime import datetime, timedelta

import requests
from lxml import etree

from .utils import STANDARD_TIME_FORMAT

PLATFORM_NAME = 'biendata'


def get_data():
    url = 'https://www.biendata.com/competition/'

    response = requests.get(url=url)
    html = response.text

    html = etree.HTML(html)
    css_list = html.cssselect('div.active ul.list li')
    data = {'name': PLATFORM_NAME}
    cps = []
    for info in css_list:
        reward = info.cssselect('div.end > span')[0].text.strip()
        if reward == "":
            continue

        name = info.cssselect('span.des_text.p0')[0].text.strip()
        url = 'https://www.biendata.com' + info.cssselect(
            'div.content h4 a')[0].attrib['href'].strip()

        deadline = info.cssselect('dl dd:nth-child(2) > span')[0].text.strip()
        deadline = deadline.split('~')[1].strip()
        FORMAT = "%Y-%m-%d"
        deadline = datetime.strptime(deadline, FORMAT) + timedelta(hours=8)
        deadline = deadline.strftime(STANDARD_TIME_FORMAT)

        cp = {
            'name': name,
            'url': url,
            'description': name,
            'deadline': deadline,
            'reward': reward
        }

        cps.append(cp)

    data['competitions'] = cps

    return data
import requests
import time
import logging

from .constants import headers


API = 'https://api.bilibili.com/x/vas/dlc_act/act/item/list?act_id={act}'


def scrape(act: int):
    logging.debug('scraping biliNFT detail of %s %s', act)
    req = requests.get(API.format(act=act),
                       timeout=10, headers=headers)
    time.sleep(3)
    return req.json()['data']


if __name__ == '__main__':
    print(scrape(101777))

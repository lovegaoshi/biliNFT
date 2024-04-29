import requests
import time
import logging

from .constants import headers


API = 'https://api.bilibili.com/x/vas/dlc_act/lottery_home_detail?act_id={act}&lottery_id={lottery}'


def scrape(act: int, lottery: int):
    logging.debug('scraping biliNFT detail of %s %s', act, lottery)
    req = requests.get(API.format(act=act, lottery=lottery),
                       timeout=10, headers=headers)
    time.sleep(3)
    return req.json()['data']


if __name__ == '__main__':
    print(scrape(101777, 101796))

import requests
import time
import logging
import json

from scrapers.constants import headers


BASIC_API = 'https://api.bilibili.com/x/vas/dlc_act/act/basic?act_id={id}'
API = 'https://api.bilibili.com/x/vas/dlc_act/lottery_home_detail?act\
_id={act}&lottery_id={lottery}'

def scrape_detail(act: int, lottery: int):
    logging.debug('scraping biliNFT detail of %s %s', act, lottery)
    req = requests.get(API.format(act=act, lottery=lottery),
                       timeout=10, headers=headers)
    time.sleep(3)
    return req.json()['data']

def scrape(last_scraped: str):
    data = {}
    res = requests.get(BASIC_API.format(id=last_scraped),
                       timeout=10, headers=headers)
    jsoned = res.json()
    if jsoned['code'] != 0:
        logging.warning(
            '%s errored out: %s.', last_scraped, json.dumps(jsoned))
        return 1
    logging.info(
        'scaped %s to be %s', last_scraped, jsoned["data"]["act_title"])
    data['basic'] = jsoned['data']
    time.sleep(1)  #
    data['list'] = [scrape_detail(last_scraped, x['lottery_id'])
                    for x in data['basic']['lottery_list']]
    return data

if __name__ == '__main__':
    print(scrape(101777))

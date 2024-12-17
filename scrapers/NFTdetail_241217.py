import requests
import logging
import json

from scrapers.constants import headers

# https://github.com/SocialSisterYi/bilibili-API-collect/issues/1155
API = 'https://api.bilibili.com/x/vas/dlc_act/asset_bag?act_id={id}'

def scrape(last_scraped: str):
    res = requests.get(API.format(id=last_scraped),
                       timeout=10, headers=headers)
    jsoned = res.json()
    if jsoned['code'] != 0:
        logging.warning(
            '%s errored out: %s.', last_scraped, json.dumps(jsoned))
        return 1
    logging.info(
        'scaped %s to be %s', last_scraped, jsoned["data"]["uname"])
    return jsoned['data']

if __name__ == '__main__':
    print(scrape(101777))

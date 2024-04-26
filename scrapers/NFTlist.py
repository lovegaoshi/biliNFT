import requests
import time
import logging

from .constants import headers

API = 'https://api.bilibili.com/x/vas/dlc_act/act/list?&scene=1&site={counts}'

def scrape(init=0, end=None):
    logging.debug('scraping masterlist of biliNFT %s to %s', init, end)    
    if end is not None and init > end:
        return []
    req = requests.get(API.format(counts=init), timeout=10, headers=headers)
    time.sleep(4)
    json = req.json()['data']
    result = [x['act_id'] for x in json['list']]
    if json['is_more']:
        if end is None or end > json['site']:
            return result + scrape(json['site'], end=end)
    return result

if __name__ == '__main__':
    print(scrape(0, 21))
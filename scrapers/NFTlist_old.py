import requests
import time
import logging

from .constants import headers

MASTER_LIST_API = 'https://api.bilibili.com/x/garb/card/subject/list?subject_id=42'

def scrape():

    res = requests.get(MASTER_LIST_API, timeout=10, headers=headers)
    jsoned = res.json()
    return [x['act_id'] for x in jsoned['data']['subject_card_list']]

if __name__ == '__main__':
    print(scrape())
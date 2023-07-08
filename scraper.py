import requests
import json
import time
import sys
import logging
from os.path import join

'''
https://api.bilibili.com/x/vas/dlc_act/act/basic?act_id={藏品id}
https://api.bilibili.com/x/vas/dlc_act/act/item/list?act_id={藏品id}
'''
BASIC_API = 'https://api.bilibili.com/x/vas/dlc_act/act/basic?act_id={id}'
LIST_API = 'https://api.bilibili.com/x/vas/dlc_act/act/item/list?act_id={id}'

try:
    with open('scraped.point') as f:
        last_scraped = json.load(f)
except Exception as e:
    logging.error(e)
    last_scraped = '100'


def save_last_scraped(scraped: str):
    logging.debug(f'saving {scraped} to disk.')
    with open('scraped.point', 'w') as f:
        json.dump(scraped, f)
    sys.exit(0)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    forcequit = 0
    data = {}
    while True:
        if forcequit > 10:
            save_last_scraped(last_scraped)
        res = requests.get(BASIC_API.format(id=last_scraped))
        jsoned = res.json()
        if jsoned['code'] != 0:
            logging.warning(
                f'{last_scraped} errored out: {json.dumps(jsoned)}.')
            if jsoned['message'] == "活动ID不存在":
                logging.info(f'{last_scraped} DNE. terminating program.')
                save_last_scraped(last_scraped)
            else:
                forcequit += 1
                logging.info(
                    f'{last_scraped} errors but message is not DNE. program will attempt to continue with a forcequit val of {forcequit}')
                time.sleep(1)
                last_scraped = str(int(last_scraped) + 1)
                continue
        logging.info(
            f'scaped {last_scraped} to be {jsoned["data"]["act_title"]}')
        data['basic'] = jsoned
        time.sleep(1)
        data['list'] = requests.get(LIST_API.format(id=last_scraped)).json()
        with open(join('data', f'BILINFT_{last_scraped}.json'), 'w') as f:
            json.dump(data, f, indent=4)
        time.sleep(1)
        last_scraped = str(int(last_scraped) + 1)

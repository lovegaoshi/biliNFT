import json
import time
import sys
import logging
import glob
from os.path import join, basename
import requests

from scrapers.NFTlist import scrape as masterlist_scrape
from scrapers.NFTdetail import scrape as detail_scrape
from scrapers.constants import headers

'''
https://api.bilibili.com/x/vas/dlc_act/act/basic?act_id={藏品id}
https://api.bilibili.com/x/vas/dlc_act/act/item/list?act_id={藏品id}
'''
BASIC_API = 'https://api.bilibili.com/x/vas/dlc_act/act/basic?act_id={id}'


def save_last_scraped(scraped: str):
    logging.debug('saving %s to disk.', scraped)
    with open('scraped.point', 'w', encoding='utf-8') as f:
        json.dump(str(int(scraped) - 1), f)
    sys.exit(0)


def write_list():
    with open('list.md', 'w', encoding='utf-8') as f:
        for jsondata in sorted(glob.glob('data/*.json')):
            try:
                nft_id = basename(jsondata)[8:-5]
                with open(jsondata, encoding='utf-8') as g:
                    loaded_data = json.load(g)
                logging.debug("now processing %s", jsondata)
                biliNFT_name = loaded_data["basic"]["act_title"]
                biliNFT_img = loaded_data["basic"]["lottery_list"][0]["lottery_image"]
                f.write(
                    f'[# {nft_id}.{biliNFT_name}](https://github.com/lovegaoshi/'
                    f'biliNFT/blob/main/data/{basename(jsondata)})\n')
                f.write(f'![{biliNFT_name}]({biliNFT_img})\n')
                f.write('\n')
            except Exception as ee:
                logging.error(ee)
                logging.error('failed to write %s. is it valid?', jsondata)


def scrape_id(last_scraped: str):
    data = {}
    res = requests.get(BASIC_API.format(id=last_scraped),
                       timeout=10, headers=headers)
    jsoned = res.json()
    if jsoned['code'] != 0:
        logging.warning(
            '%s errored out: %s.', last_scraped, json.dumps(jsoned))
        if jsoned['message'] == "活动ID不存在":
            logging.info('%s DNE. terminating program?', last_scraped)
            last_scraped = str(int(last_scraped) + 1)
            time.sleep(1)
            # save_last_scraped(last_scraped)
            return 1
        else:
            last_scraped = str(int(last_scraped) + 1)
            logging.info(
                '%s errors but message is not DNE. program will attempt to continue', last_scraped)
            time.sleep(1)
            return 1
    logging.info(
        'scaped %s to be %s', last_scraped, jsoned["data"]["act_title"])
    data['basic'] = jsoned['data']
    time.sleep(1)  # 
    data['list'] = [detail_scrape(last_scraped, x['lottery_id'])
                    for x in data['basic']['lottery_list']]
    with open(join('data', f'BILINFT_{last_scraped}.json'), 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    return 0


def old_scrape():
    try:
        with open('scraped.point', encoding='utf-8') as f:
            last_scraped = json.load(f)
    except Exception as e:
        logging.error(e)
        last_scraped = '100'

    forcequit = 0
    saved_last_scraped = last_scraped
    while True:
        if forcequit > 10:
            write_list()
            save_last_scraped(saved_last_scraped)
        forcequit += scrape_id(last_scraped)
        saved_last_scraped = last_scraped = str(int(last_scraped) + 1)


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description="ina music segment")
    parser.add_argument("--id", type=str,
                        help="file path or weblink", nargs='+', default=[])
    args = parser.parse_args()

    logging.basicConfig(level=logging.DEBUG)
    if (len(args.id) > 0):
        nft_list = args.id
    else:
        nft_list = masterlist_scrape()
    scraped_nft = [int(basename(x)[8:-5]) for x in glob.glob('data/*.json')]
    for nft_id in nft_list:
        if nft_id not in scraped_nft:
            logging.info('scraping %s', nft_id)
            scrape_id(nft_id)

    write_list()
    # old_scrape()

import requests
import sys
import json

if __name__ == '__main__':
    res = requests.get(sys.argv[1], timeout=60)
    with open('biliEmote.json', 'w', encoding='utf-8') as f:
        json.dump(res.json(), f)

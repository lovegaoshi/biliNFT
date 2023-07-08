import glob
import json

for i in glob.glob('data/*.json'):
    json.dump(json.load(open(i, encoding='utf-8')), open(i, 'w', encoding='utf-8'), indent=4,
              ensure_ascii=False)

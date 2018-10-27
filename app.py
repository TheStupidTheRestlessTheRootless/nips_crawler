# -*- coding: UTF-8 -*-
from crawler import get_nips_records
from config import Configs
from tools import serialize_instance
import json

if __name__ == "__main__":
    print('nips_crawler')
    l = get_nips_records(Configs.years)
    json_str = json.dumps([serialize_instance(x) for x in l])
    with open('output.json', 'w') as f:
        print(json_str, file=f)
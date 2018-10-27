# -*- coding: UTF-8 -*-
from crawler import get_nips_records
from config import Configs

if __name__ == "__main__":
    print('nips_crawler')
    l = get_nips_records(Configs.years)

# -*- coding: UTF-8 -*-
import requests
from bs4 import BeautifulSoup
import re
import time
from session import session
from model import Record, Poster
from config import Configs

poster_url = "https://nips.cc/Conferences/{0}/Schedule?type=Poster"
poster_detail_url="https://nips.cc/Conferences/2016/Schedule?showEvent={0}"
speaker_detail_url="https://nips.cc/Conferences/2017/Schedule?showSpeaker={0}"
article_list_url="http://papers.nips.cc/author/{0}-{1}"


# get the poster id list
def get_year_posters(year):
    print("get poster of year: " + year)
    poster_list = []
    try:
        r = session.get(poster_url.format(year))
        soup = BeautifulSoup(r.text, features="html.parser")
        tags = soup.find_all('div', {"onclick": re.compile(r"showDetail.*")})
        for a in tags:
            ids = re.compile(r"[\d | -]+").findall(a["onclick"])
            title = a.find('div', class_='maincardBody')
            if len(ids)>0:
                poster_list.append(Poster(ids[0], title.text))
    except requests.exceptions.RequestException as e:  # This is the correct syntax
        print(e)
    return poster_list

# get speaker id list in poster detail page
def get_speakers(poster, speaker_dict = {}):
    print("get speakers by poster: " + poster.id)
    try:
        r = session.get(poster_detail_url.format(poster.id))
        soup = BeautifulSoup(r.text, features="html.parser")
        tags = soup.find_all('button', {"onclick": re.compile(r"showSpeaker.*")})
        for i, a in enumerate(tags):
            ids = re.compile(r"[\d | -]+").findall(a["onclick"])
            if len(ids)>0 :
                id = ids[0]
                if (id not in speaker_dict):
                    speaker_dict[id] = Record(ids[0]) 
                record = speaker_dict[id]
                if i == 0 and (poster.title not in record.first):
                    record.add_first(poster.title)
                if i > 0 and (poster.title not in record.other):
                    record.add_other(poster.title)
                get_speakers_detail(record)
    except requests.exceptions.RequestException as e:  # This is the correct syntax
        print(e)
    return speaker_dict

# get speaker organization by speaker id
def get_speakers_detail(record):
    print("get speaker detail: " + record.id)
    try:
        r = session.get(speaker_detail_url.format(record.id))
        soup = BeautifulSoup(r.text, features="html.parser")
        tags = soup.find_all('div', class_="maincard")
        for t in tags:
            record.name = t.h3.text
            record.organization = t.h4.text
    except requests.exceptions.RequestException as e:  # This is the correct syntax
        print(e)
    # 延迟一会儿，避免服务器压力过大
    time.sleep(Configs.sleep_interval)

# get speaker articles by speaker name and id
def get_speaker_articles(record):
    print("get speaker articles: " + record.id)
    print(article_list_url.format(record.name.replace(' ', '-').lower(), record.id))
    try:
        r = session.get(article_list_url.format(record.name.replace(' ', '-').lower(), record.id))
        soup = BeautifulSoup(r.text, features="html.parser")
        tags = soup.find_all('li', class_="paper")
        for li in tags:
            print(li)
    except requests.exceptions.RequestException as e:  # This is the correct syntax
        print(e)

def merge_author(d = {}):
    merged_d = {}
    for a in d.items():
        r = a[1]
        k = "{0}_{1}".format(r.name.replace(" ", '-').lower(), r.organization.replace(' ', "_").lower())
        if k not in merged_d:
            merged_d[k] = Record(k)
            merged_d[k].name = r.name
            merged_d[k].organization = r.organization
        merged_d[k].first.extend(r.first)
        merged_d[k].other.extend(r.other)
    return merged_d

def get_nips_records(years):
    speaker_dict = {}
    for y in years:
        posters = get_year_posters(y)
        for p in posters:
            get_speakers(p, speaker_dict)
    
    merged_d = merge_author(speaker_dict)
    return list(merged_d.values())
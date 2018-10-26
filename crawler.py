# -*- coding: UTF-8 -*-
import requests
from bs4 import BeautifulSoup

poster_url = "https://nips.cc/Conferences/{0}/Schedule?type=Poster"
poster_detail_url="https://nips.cc/Conferences/2016/Schedule?showEvent={0}"
speaker_detail_url="https://nips.cc/Conferences/2017/Schedule?showSpeaker={0}"

# get the poster id list
def get_year_posters(year):
    r = requests.get(poster_url.format(year))
    soup = BeautifulSoup(r.text)
    tags = soup.find_all('a')
    print(tags)
    for a in tags:
        print(a)

# get speaker id list in poster detail page
def get_speakers(poster_id):
    print(poster_id)

# get speaker organization by speaker id
def get_speakers_detail(speaker_id):
    print(speaker_id)

def get_nips_records(years):
    records = []
    for y in years:
        get_year_posters(y)
    return records
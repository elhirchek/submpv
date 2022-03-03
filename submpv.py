# standard library
import zipfile
from re import search
from os import remove,chdir
from sys import argv,exit as sys_exit
from difflib import SequenceMatcher
# third party library
import requests
from bs4 import BeautifulSoup as bs

# help
if argv or "-h" in argv or "--help" in argv :
    print("Subscene to mpv usage:\n\tsub \'tv show name\'\nfor example:\n\tsub \'breaking.bad.s01e07\'")
    sys_exit(0)

# split name to actual_name/season/episode
def get_s_ep(name):
    s_ep = [name[:name.index(search(r's\d\d|S\d\d',name).group())],search(r's\d\d|S\d\d',name).group(),search(r'e\d\d|E\d\d',name).group()]
    return s_ep

# scrap func
def scrape(url,name=""):
    if name:
        soup = bs(requests.get(url,params={'query':name}).content,'html.parser')
    else:
        soup = bs(requests.get(url).content,'html.parser')
    return soup

# query url func
def get_query_url(soup,target,season):
    sea = {'S01':' First','S02':' Second','S03':' Third','S04':' Fourth','S05':' Fifth','S06':' Sixth','S07':' Seventh','S08':' Eighth'}
    urls = [i for i in soup.find_all('a',href=True,limit=16) if str(i.get('href')).startswith('/subtitles')]
    names = [i.text for i in urls]
    split_names = [i.text.split('-') for i in urls]
    for i in split_names:
        if len(i)>=2:
            if SequenceMatcher(None, i[0].lower(), target.lower()).ratio() >= 0.7 and str(i[1]).startswith(sea[season.upper()]):
                return urls[names.index(i[0]+'-'+i[1])].get('href')
        elif i == split_names[-1]:
            print('not found!')
            sys_exit(0)
                
# episode url func
def ep_url(soup,get_url,ep):
    urls = [i for i in soup.find_all('a',href=True) if str(i.get('href')).startswith(f'{get_url}/arabic')]
    for i in urls:
        if search(r'e\d\d|e\d',i.span.find_next_sibling('span').text.lower()) != None:
            if search(r'e\d\d|e\d',i.span.find_next_sibling('span').text.lower()).group().lower() == ep.lower():
                return i.get('href')
        elif i == urls[-1]:
            print('not found!')
            sys_exit(0)

# download subtitle func
def dw_sub(soup):
    div = soup.find("div", {"class": "download"})
    down_link = "https://subscene.com" + div.find("a").get("href")
    down_sub = requests.get(down_link, stream=True).content
    if '-d' in argv:
        arg = argv.index('-d') + 1
        chdir(argv[arg])
    with open('sub.zip','wb') as f:
        f.write(down_sub)
    with zipfile.ZipFile('sub.zip', "r") as f:
        f.extractall()
    remove('sub.zip')
    print('done')

# Variables
search_url = 'https://subscene.com/subtitles/searchbytitle'
url = 'https://subscene.com'
name = argv[-1]
s_ep = get_s_ep(name)

# query
query_soup = scrape(search_url,s_ep[0])
query_url = get_query_url(query_soup,s_ep[0],s_ep[1])

# find match ep
ep_soup = scrape(url+query_url)
ep_url = ep_url(ep_soup,query_url,s_ep[-1])

# download sub
dl_soup = scrape(url+ep_url)
dw_sub(dl_soup)

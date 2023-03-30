#!/usr/bin/python

# standard library
import argparse
import zipfile
from re import search
from os import remove,chdir
from sys import argv,exit as sys_exit
from difflib import SequenceMatcher,get_close_matches
# third party library
from guessit import guessit
import requests
from bs4 import BeautifulSoup as bs

# help
parser = argparse.ArgumentParser(
    description="submpv is a download/add subtitle from subscence",
    epilog="Author:yassin-l",
)
parser.add_argument('name',help='the show name to download sub for should be in \"\" with no spaces like:"name.sxex" or the movie name with in \"\" with year of release like this:"movie (year)"')
parser.add_argument('-d','--directory',metavar="",type=str,help='choose where to download sub by default:current directory')
parser.add_argument('-l','--lang',metavar="",choices=['ar','en'],help='select which language to filter with',default='ar')
args = parser.parse_args()

# var
url = 'https://subscene.com'
headers = {
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36"
        }

# scrap func
def scrape(url:str=None,name:str=None): 
    if name:
        url = 'https://subscene.com/subtitles/searchbytitle'
        request = requests.get(url,params={'query':name},headers=headers)

    else:
        request = requests.get(url,headers=headers)

    if request.status_code == 200:
        return bs(request.content,'html.parser')

    print('connection error try again')
    sys_exit()

# get query url
def get_query_url(soup,name):
    if name.get('type',None) == 'episode':
        seasons = {1:'first-season',2:'second-season',3:'third-season',4:'fourth-season',5:'fifth-season',6:'sixth-Season',7:'seventh-season',8:'eighth-season'}
        urls = [i for i in soup.find_all('a',href=True,limit=16) if str(i.get('href')).startswith('/subtitles')]
        matches = [SequenceMatcher(None,i.get('href'),f"{name['title']}-{seasons[name['season']]}").ratio() for i in urls]
        return urls[matches.index(max(matches))].get('href')

    else:
        urls = [i for i in soup.find_all('a',href=True,limit=16) if str(i.get('href')).startswith('/subtitles')]
        if name.get('year',None):
            matches = [SequenceMatcher(None,i.text,f"{name['title']} - ({name['year']})").ratio() for i in urls]
        else:
            matches = [SequenceMatcher(None,i.text,f"{name['title']})").ratio() for i in urls]
        return urls[matches.index(max(matches))].get('href')

    print('not found')
    sys_exit(0)

## get episode url 
def ep_url(url:str,soup,name):
    if name.get('type',None) == 'episode':
        langs = {'ar':'arabic','en':'english','fr':'french'}
        urls = [i for i in soup.find_all('a',href=True) if str(i.get('href')).startswith(f'{url}/{langs.get("args.lang","ar")}')]
        num = f"0{name['episode']}" if len(str(name['episode'])) < 2 else name['episode']
        for i in urls:
            _name = search(r'e?{n}'.format(n=num),i.span.find_next_sibling('span').text.lower())
            if _name:
                return i.get('href')
    else:
        urls = [i for i in soup.find_all('a',href=True) if str(i.get('href')).startswith(f'{url}/{args.lang}')]
        _url = []
        # filter based on edition and source using a dic
        #for i in urls:
        #    if search(r'{}'.format(name['title']).lower(),i.span.find_next_sibling('span').text.lower()):
        #        _name.append(i.get('href'))
        if name.get('source',None):
            for i in urls:
                _name = search(r'{}'.format(name['title']).lower(),i.span.find_next_sibling('span').text.lower())
                _source = search(r'{}'.format(name['source']).lower(),i.span.find_next_sibling('span').text.lower())
                if _name and _source:
                    return i.get('href')
        for i in urls:
            _name = search(r'{}'.format(name['title']).lower(),i.span.find_next_sibling('span').text.lower())
            if _name:
                return i.get('href')
    print('not found!')
    sys_exit(0)

## download subtitle 
def dw_sub(soup):
    div = soup.find("div", {"class": "download"})
    down_link = url + div.find("a").get("href")
    down_sub = requests.get(down_link,headers=headers, stream=True).content
    if args.directory:
        chdir(args.directory)
    with open('sub.zip','wb') as f:
        f.write(down_sub)
    with zipfile.ZipFile('sub.zip', "r") as f:
        f.extractall()
    remove('sub.zip')
    print('done')

def main():
    # parsing giving name
    name = guessit(args.name)

    # get sub first page
    first_url = get_query_url(scrape(name=name['title']),name)

    # getting episode url
    episode_url = ep_url(first_url,scrape(url+first_url),name)

    # downloading subtitle
    dw_sub(scrape(url+episode_url))


if __name__ == "__main__":
    main()

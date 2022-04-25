# standard library
import argparse
import zipfile
from re import search
from os import remove,chdir
from sys import argv,exit as sys_exit
from difflib import SequenceMatcher
# third party library
from guessit import guessit
import requests
from bs4 import BeautifulSoup as bs

# help
parser = argparse.ArgumentParser(
    description="submpv is a dow/add sub from subscence",
    epilog="Author:yassi-l",
)
parser.add_argument('name',help='the show name to download sub for should be in \"\" with no spaces like:"name.sxex"')
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
        if request.status_code == 200:
            soup = bs(request.content,'html.parser')
    else:
        request = requests.get(url,headers=headers)
        if request.status_code == 200:
            soup = bs(request.content,'html.parser')
    if soup:
        return soup
    print('connection error try again')
    sys_exit()

# get query url
def get_query_url(soup,name):
    if name['type'] == 'episode':
        seasons = {1:' First',2:' Second',3:' Third',4:' Fourth',5:' Fifth',6:' Sixth',7:' Seventh',8:' Eighth'}
        urls = [i for i in soup.find_all('a',href=True,limit=16) if str(i.get('href')).startswith('/subtitles')]
        names = [i.text.split('-') for i in urls if len(i.text.split('-')) >= 2]
        for x,i in enumerate(names):
            if SequenceMatcher(None, i[0].lower(), name['title'].lower()).ratio() >= 0.7 and str(i[1]).startswith(seasons[name['season']]):
                return urls[x].get('href')

    elif name['type'] == 'movie':
        urls = [i for i in soup.find_all('a',href=True,limit=16) if str(i.get('href')).startswith('/subtitles')] # add check for the year
        names = [i.text for i in urls]
        for x,i in enumerate(names):
            if SequenceMatcher(None, i.lower(), name['title'].lower()).ratio() >= 0.8:
                return urls[x].get('href')

    print('not found')
    sys_exit(0)

## get episode url 
def ep_url(url:str,soup,name):
    if name['type'] == 'episode':
        langs = {'ar':'arabic','en':'english'}
        urls = [i for i in soup.find_all('a',href=True) if str(i.get('href')).startswith(f'{url}/{langs[args.lang]}')]
        for i in urls:
            _name = search(r'e{n}'.format(n=name['episode']),i.span.find_next_sibling('span').text.lower())
            if _name and _name.group() == 'e'+str(name['episode']):
                return i.get('href')
    elif name['type'] == 'movie':
        urls = [i for i in soup.find_all('a',href=True) if str(i.get('href')).startswith(f'{url}/{args.lang}')]
        for i in urls:
            _name = search(r'{}'.format(name['title']),i.span.find_next_sibling('span').text.lower())
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
    print('done',end='')

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
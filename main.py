import requests
from bs4 import BeautifulSoup
# karbar=input().split()
page = requests.get(f'https://30nama.com/genre/drama')
soup = BeautifulSoup(page.text, 'html.parser')

links = 'https://30nama.com/series/12382/Breaking-Bad-2008'

def story(links):
    # eachlink=links[movienames.index(film)]
    link=requests.get(links)
    soups=BeautifulSoup(link.text,'html.parser')
    stories=soups.find_all('div',class_='content')
    if not stories==[] :
        print(stories[2].text)

story(links)

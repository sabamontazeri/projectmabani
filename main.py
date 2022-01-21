import requests
from bs4 import BeautifulSoup
import re

genre = input()
page = requests.get(f'https://30nama.com/genre/{genre}')
soup = BeautifulSoup(page.text, 'html.parser')

film = input()


everylinks=[]
def linkfilm(soup, everylinks):
    links = soup.find_all('a', draggable='false')
    for i in range(len(links)):
        eachlink = links[i]['href']
        everylinks.append(eachlink)
    return everylinks
links = linkfilm(soup, everylinks)



def movienames(links):
    movie = []
    links = links[:10]
    for item in links:
        link = requests.get('https://30nama.com' + item)
        soups = BeautifulSoup(link.text, 'html.parser')
        moviename = soups.find_all('h3', class_='bd-large persian-title color-secondary')
        movie.append(moviename[0].text.strip())
    return movie
print(movienames(links))


eachlink = links[movienames(links).index(film)]

import requests
from bs4 import BeautifulSoup
import re

genre = input()
page = requests.get(f'https://30nama.com/genre/{genre}')
soup = BeautifulSoup(page.text, 'html.parser')

film = input()


everylinks=[]
# movie links:
def linkfilm(soup, everylinks):
    links = soup.find_all('a', draggable='false')
    for i in range(len(links)):
        eachlink = links[i]['href']
        everylinks.append(eachlink)
    return everylinks
links = linkfilm(soup, everylinks)


# movie names:
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

# story of the movie:
def story(eachlink):
    link = requests.get('https://30nama.com' + eachlink)
    soups = BeautifulSoup(link.text, 'html.parser')
    stories = soups.find_all('div', class_='content')
    if not stories == []:
        print(stories[2].text.strip())

story(eachlink)

# actors' names:
def actors(eachlink):
    link = requests.get('https://30nama.com' + eachlink)
    soups = BeautifulSoup(link.text, 'html.parser')
    actors = soups.find_all('h5', class_="bd-sm")
    if actors != []:
        for i in range(0, len(actors), 2):
            print(re.findall('.*\n', actors[i].text)[1].strip())
actors(eachlink)

print()

# writer and creator:
def crews(eachlink):
    link = requests.get('https://30nama.com' + eachlink)
    soups = BeautifulSoup(link.text, 'html.parser')
    crews = soups.find_all('a', class_="child-link")
    if crews != []:
        print(re.findall('.*\n', crews[8].text)[1].strip())
        print(re.findall('.*\n', crews[len(crews)-1].text)[1].strip())

crews(eachlink)


from selenium import webdriver
from selenium.webdriver.common.by import By
import re

karbar = input().split()

driver = webdriver.Firefox(executable_path='C:\\Users\\Sportg\\Desktop\\geckodriver.exe')
driver.get(f'https://www.namava.ir/search?type={karbar[0]}&country={karbar[1]}&genre={karbar[2]}')
# driver.get(f'https://www.namava.ir/search?query={film}')


movienames = []
film = input()
elements = driver.find_elements(By.TAG_NAME, 'img')

for element in elements:
    movienames.append(element.get_attribute('title').strip())
print(movienames)

everylinks = []
def linkfilm(driver, everylinks):
    links = driver.find_elements(By.TAG_NAME, 'a')
    for item in links:
        eachlink = item.get_attribute('href')
        everylinks.append(eachlink)
    everylinks = everylinks[4:]
    return everylinks
links = linkfilm(driver,everylinks)


def story(links):
    eachlink = links[movienames.index(film)]
    driver.get(eachlink)
    content = driver.find_elements(By.CLASS_NAME, 'vertical-center')
    try:
        print(re.findall(".*\n", content[1].text)[2])
    except:
        pass
story(links)
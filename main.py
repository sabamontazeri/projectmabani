from selenium import webdriver
from selenium.webdriver.common.by import By

karbar = input().split()
driver = webdriver.Firefox(executable_path='C:\\Users\\Sportg\\Desktop\\geckodriver.exe')
driver.get(f'https://www.namava.ir/search?type={karbar[0]}&country={karbar[1]}&genre={karbar[2]}')

movienames = []
film = input()
elements = driver.find_elements(By.TAG_NAME, 'img')

for element in elements:
    movienames.append(element.get_attribute('title'))
print(movienames[:20])


everylinks = []
def linkfilm(driver, everylinks):
    links = driver.find_elements(By.TAG_NAME, 'a')
    for item in links:
        eachlink = item.get_attribute('href')
        everylinks.append(eachlink)
    return everylinks
links = linkfilm(driver, everylinks)
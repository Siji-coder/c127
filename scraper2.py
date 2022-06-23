from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
import pandas as pd
import requests
import csv

START_URL = "https://exoplanets.nasa.gov/exoplanet-catalog/"
browser = webdriver.Chrome("/Users/91963/venv/chromedriver")
browser.get(START_URL)
time.sleep(10)
#add all the relevant columns
headers = ["name", "light_years_from_earth", "planet_mass", "stellar_magnitude", "discovery_date","hyperlink"]
planet_data = []
def scrape():
    
    for i in range(1,5):
        soup = BeautifulSoup(browser.page_source, "html.parser")

        #to check, the scrapping done page one by one
        current_page_num = int(soup.find_all("input", attrs={"class", "page_num"})[0].get("value"))
        if current_page_num < i:
            browser.find_element(By.XPATH, value='//*[@id="primary_column"]/div[1]/div[2]/div[1]/div/nav/span[2]/a').click()
                
        elif current_page_num > i:
            browser.find_element(By.XPATH, value='//*[@id="primary_column"]/div[1]/div[2]/div[1]/div/nav/span[1]/a').click()
                
        else:
            break

           
        for ul_tag in soup.find_all("ul", attrs={"class", "exoplanet"}):
            li_tags = ul_tag.find_all("li")
            temp_list = []
            for index, li_tag in enumerate(li_tags):
                if index == 0:
                    temp_list.append(li_tag.find_all("a")[0].contents[0])
                else:
                    try:
                        temp_list.append(li_tag.contents[0])
                    except:
                        temp_list.append("")
            #add the href to the temp_list
            hyperlink_li_tag=li_tag[0]
            temp_list.append("https://exoplanets.nasa.gov"+hyperlink_li_tag.find_all("a",href=True)[0]["href"])
            planet_data.append(temp_list)
        browser.find_element_by_xpath('//*[@id="primary_column"]/div[1]/div[2]/div[1]/div/nav/span[2]/a').click()
        print(planet_data[0])
    """with open("scrapper_2.csv", "w") as f:
        csvwriter = csv.writer(f)
        csvwriter.writerow(headers)
        csvwriter.writerows(planet_data)"""
scrape()
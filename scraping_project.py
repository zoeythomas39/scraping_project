# loading programs

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

from bs4 import BeautifulSoup
from random import randint
import time
import random
import csv
import os

# installing driver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# specifying links of pages to be scraped

men_lead = 'https://aaspeechesdb.oscars.org/results.aspx?QB5=AND&QF5=transcript+%7c+acceptorlink+%7c+ed+note+%7c+name+%7c+film+title+%7c+song+title+%7c+category+index+%7c+acceptor+statement+%7c+category+exact+%7c+name+authority+%7c+winner+statement+%7c+year+term&QI5=&QB1=AND&QF1=name+%7c+winner+statement+%7c+name+authority&QI1=&QB2=AND&QF2=film+title&QI2=&QB3=AND&QF3=category+index&QI3=%3d%22Actor+Leading+Role%22&QB0=AND&QF0=year+term&QI0=&QF6=video+link&AC=QBE_QUERY&TN=aatrans&RF=WebReportList&DF=WebReportOscars&MR=0&BU=https%3a%2f%2faaspeechesdb.oscars.org%2f&'
women_lead = 'https://aaspeechesdb.oscars.org/results.aspx?QB5=AND&QF5=transcript+%7c+acceptorlink+%7c+ed+note+%7c+name+%7c+film+title+%7c+song+title+%7c+category+index+%7c+acceptor+statement+%7c+category+exact+%7c+name+authority+%7c+winner+statement+%7c+year+term&QI5=&QB1=AND&QF1=name+%7c+winner+statement+%7c+name+authority&QI1=&QB2=AND&QF2=film+title&QI2=&QB3=AND&QF3=category+index&QI3=%3d%22Actress+Leading+Role%22&QB0=AND&QF0=year+term&QI0=&QF6=video+link&AC=QBE_QUERY&TN=aatrans&RF=WebReportList&DF=WebReportOscars&MR=0&BU=https%3a%2f%2faaspeechesdb.oscars.org%2f&'
men_support = 'https://aaspeechesdb.oscars.org/results.aspx?QB5=AND&QF5=transcript+%7c+acceptorlink+%7c+ed+note+%7c+name+%7c+film+title+%7c+song+title+%7c+category+index+%7c+acceptor+statement+%7c+category+exact+%7c+name+authority+%7c+winner+statement+%7c+year+term&QI5=&QB1=AND&QF1=name+%7c+winner+statement+%7c+name+authority&QI1=&QB2=AND&QF2=film+title&QI2=&QB3=AND&QF3=category+index&QI3=%3d%22Actor+Supporting+Role%22&QB0=AND&QF0=year+term&QI0=&QF6=video+link&AC=QBE_QUERY&TN=aatrans&RF=WebReportList&DF=WebReportOscars&MR=0&BU=https%3a%2f%2faaspeechesdb.oscars.org%2f&'
women_support = 'https://aaspeechesdb.oscars.org/results.aspx?QB5=AND&QF5=transcript+%7c+acceptorlink+%7c+ed+note+%7c+name+%7c+film+title+%7c+song+title+%7c+category+index+%7c+acceptor+statement+%7c+category+exact+%7c+name+authority+%7c+winner+statement+%7c+year+term&QI5=&QB1=AND&QF1=name+%7c+winner+statement+%7c+name+authority&QI1=&QB2=AND&QF2=film+title&QI2=&QB3=AND&QF3=category+index&QI3=%3d%22Actress+Supporting+Role%22&QB0=AND&QF0=year+term&QI0=&QF6=video+link&AC=QBE_QUERY&TN=aatrans&RF=WebReportList&DF=WebReportOscars&MR=0&BU=https%3a%2f%2faaspeechesdb.oscars.org%2f&'

categories = [men_lead,women_lead,men_support,women_support]

# defining function; identifying and clicking button on page to select first speech

def get_speech_info(input):

    s = randint(2,4)

    driver.get(input);

    button_list = driver.find_element(By.ID, "main").find_elements(By.TAG_NAME,"a")

    button = button_list[5]

    time.sleep(s)
    button.click()
    time.sleep(s)

# opening file for appending

    oscars_file = open('oscarspeeches.csv','a')

# selecting facts about year, category, film title and winner 

    while True:

        # making soup:

        page = driver.page_source
        soup = BeautifulSoup(page, "html.parser")
        facts = soup.select('[style*="margin:.3em 0"]')

        # using for-loop to adjust line spacing for optimal formatting in text file ...

        facts_text = []

        for i in range(4):
            facts_text.append(facts[i].text)

        replacements = {
            "Year: ": "",
            "Category: ": "",
            "Film Title: ": "",
            "Winner: ": "",
            "\n":"",
            "Actress in a Leading Role":"Actress",
            "Actor in a Leading Role":"Actor"
        }

        for i in range(len(facts_text)):
            for old, new in replacements.items():
                facts_text[i] = facts_text[i].replace(old, new)

        # moving on to select text of actual speech

        speeches = driver.find_element(By.CLASS_NAME, "MInormal")

        # we must separate [bracketed] stage directions that weren't part of the actual speech

        # first, we replace the brackets with special characters

        speech_text_list = speeches.text.replace("[","~@").replace("]","@~").split("~")

        # we make an empty list where the bracket-less words will go:

        speech_text_list_no_brackets = []

        # then, we loop the parts of the speech that WEREN'T formerly included in the brackets into the new list

        for i in range(len(speech_text_list)):
            if "@" not in speech_text_list[i]:
                speech_text_list_no_brackets.append(speech_text_list[i].strip())

            # finally, we join the strings back together into complete speeches

            joined_speeches = str(" ".join(speech_text_list_no_brackets))

        # we don't want hyphens surrounded by spaces to be counted as words, so we have to get rid of them

        words_no_hyphens = []
        words = joined_speeches.split()
        for i in range(len(words)):
            if words[i] != "–":
                words_no_hyphens.append(words[i])

        # now, we can find the length of each speech. we subtract the name of the speaker.
        if len(words_no_hyphens) == 0:
            word_count = "N/A"
        else:
            # Count words only before the first parentheses
            winner_text = joined_speeches.split(':')[0].strip()  # Get text before '('
            print(words_no_hyphens)
            print(winner_text)
            word_count = str(len(words_no_hyphens) - len(winner_text.split()))
        
        header_written = False  # Flag to track if the header has been written

        file_path = 'oscarspeeches.csv'

        # Open the file in append mode
        with open(file_path, 'a', newline='') as oscars_file:
            oscarWriter = csv.writer(oscars_file)

            # Write the header only if the file is empty
            if os.path.getsize(file_path) == 0:
                oscarWriter.writerow(['year', 'category', 'film', 'winner', 'words'])

            # Writing facts + word count
            facts_plus_words = facts_text + [word_count]
            oscarWriter.writerow(facts_plus_words)

        # we stop the code when we get to the most recent year (2023)
        
        if "2023" in facts[0].text:
            break
        
        # finally, we select the "next" button using selenium to scrape the next page, close the file and quit the driver

        button2 = driver.find_element(By.LINK_TEXT, "Next")
        button2.click()
        time.sleep(s)

    oscars_file.close()
    time.sleep(s)

for i in range(len(categories)):
    get_speech_info(categories[i])

driver.quit()
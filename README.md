# Oscars acceptance speech scrape 

This project uses data from the [Academy Awards Acceptance Speech Database](https://aaspeechesdb.oscars.org/). The data set includes acceptance speech transcripts from over 1,500 onstage acceptance speeches given by winners and acceptors.

Speeches in the data set range from the early 1940s to the second-most-recent ceremony in 2023. It has not yet been updated with the most recent ceremony's speeches.

## Scraping goal

With this project, I aimed to discover which actors and actresses throughout the ceremony's history have given the longest speeches in number of words. By scraping the name, category, year, movie and word count for each speech, I could search for trends in the data — for example: 

+ Have speeches lengthened or shortened over time?
+ Do speech lengths vary by gender?
+ Do speech lengths vary by category?
+ What have been some of the longest and shortest speeches in history?

## Broad steps


### Installations

Before running the code, I installed these programs:

- Python 3.x
- Selenium
- BeautifulSoup4
- webdriver-manager

### Step 1: Importing Libraries
First, I imported the necessary libraries for web scraping, data storage, and timing functions:
```python
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
import random
import csv
import os
```

### Step 2: Installing the Driver
Then, I installed the Chrome WebDriver using `webdriver-manager` to make setup easier:
```python
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
```

### Step 3: Defining URLs
I defined four URLs, each for a different major Oscar category: Best Actor (Lead Role), Best Actress (Lead Role), Best Actor (Supporting Role) and Best Actress (Supporting Role).

```python
categories = [men_lead, women_lead, men_support, women_support]
```

### Step 4: The `get_speech_info()` Function
Most of this script is wrapped in one function, which scrapes speech data from a specific URL for a specific award category. These are the tasks inside the function:

1. **Opening the URL**
   - First, the Selenium driver goes to the inputted link using `driver.get(input);`, which is the page for all winners for a specific award category. There, it selects the first speech entry after finding the link using `find_element(By.ID, "main").find_elements(By.TAG_NAME,"a")` and clicks it using the `click()` function.

2. **Making Soup**
   - Next, I needed to extract Year, Category, Film Title, and Winner and cleaned them up for consistency. I started a `while True` loop to ensure the function would keep running continuously through the speeches. Then, I used `BeautifulSoup` to identify HTML elements on the page.

3. **Speech Text Cleaning**
    - I found the facts I needed using the `select()` function and appended the text from each into a new list.
    - I used several for-loops on that new list with the `range()`, `len()` and `replace` functions to loop over the gathered facts, taking out unecessary elements like the clarifier before each fact. I also noticed the "Actress" category switched to "Actress in a Leading Role" after a few decades, so I standardized that category so it would remain the same over the years.
    - I then used the Selenium `find_element` function to find each speech.
    - I edited it to remove bracketed stage directions — which don't count as part of the word count because they weren't technically said by the winner. (For example, a stage direction like [audience laughter] can't fairly be included as part of the speech.)
    - This involved more `range()`, `len()` and `replace` functions, along with for-loops.

4. **Word Count Calculating**
   - Next, I calculated the total number of words in the speech — excluding the presenter's name, which is listed at the start of each speech, separated by a colon.
   - I did so using the `split()` function to separate the speeches word-by-word, then used `len()` to find the length of each new list of words. I had to account for some issues, like hyphens surrounded by spaces being counted as their own word, which I solved using `remove()`.

5. **Writing Results to CSV**
   - I wrote the data, row by row, into a CSV file called `oscarspeeches.csv`, using the code `oscarWriter.writerow(facts_plus_words)`.
   - `facts_plus_words` was a concotenated list of each of the four facts plus the word count.
   - I also added a header row, using `if os.path.getsize(file_path) == 0:` to make sure the function didn't rewrite the header every time it begun a new loop. 

6. **Moving to Next Page**
   - Using Selenium to find the "Next" button, the function keeps navigating through the pages until it reaches the year 2023. I did this using 
   
   `if "2023" in facts[0].text:\break`
            
    - There, it stops automatically to avoid causing errors in Python.

## Unexpected challenges

I faced a **lot** of challenges while completing this project. First, I didn't understand how to select elements with Selenium, nor did I realize the commands were different than they were for BeautifulSoup. It took me hours just to figure out how to click a single link with Selenium.

After I got down a basic understanding of how to use Selenium, I faced another problem when I realized I couldn't just use the text in the speeches as-is for the word count, because it included bracketed stage directions. It took a lot of creative use of the split() function, which I actually had to doodle out on a napkin before writing, to figure out how I could break the bracketed text out of each speech.

Other little issues arose along the way — for example, I had to figure out how to get rid of the presenter's name from the word count; how to standardize the changing acting categories; how to account for hyphens separated by spaces being treated as individual words; how to make the loop stop at 2023; how to write the header row once without making it repeat in the CSV file; etc.
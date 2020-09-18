# web-scraping-challenge

This application scrapes NASA websites for data related to the Mission to Mars and displays that info in a single HTML page

### Step 1: Scraping
mission_to_mars.ipynb contains the code used to scrape the sites. It can be used to find the latest news, space images, Mars facts, and information on the 4 hemispheres of Mars.

### Step 2: MongoDB & Flask Application
scrap_mars.py converts the mission_to_mars jupyter notebook into a Python script. It returns a python dictionary containing all of the scraped data.
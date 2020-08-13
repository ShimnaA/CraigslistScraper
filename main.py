from bs4 import BeautifulSoup
import requests
import pandas as pd
import lxml


# Webpage we're scraping
#base_url = "https://losangeles.craigslist.org/search/hhh?query=ping+pong"
base_url = "https://honolulu.craigslist.org/search/oah/sss?query=cars&sort=rel"

# Send get http request
page = requests.get(base_url)

# Verify we had a successful get request call
if page.status_code == requests.codes.ok:

    # Get the whole page.
    bs = BeautifulSoup(page.text, 'lxml')


# Get all listings on this page
containing_div = bs.find('div', class_='content')

list_of_listings = containing_div.find('ul', class_='rows')

all_postings = list_of_listings.find_all('li', class_='result-row')

# Dictionary to hold the data
data = {
    'Title': [],
    'Price': [],
    }

#
for posting in all_postings:

    # Get the Title of the FIRST posting, then add it to our dictionary
    title = posting.find('a', class_='result-title hdrlnk').text

    if title:
        data['Title'].append(title)
    else:
        data['Title'].append('N/A')

    # Get the Price of the FIRST posting, then add it to our dictionary
    price = posting.find('span', class_='result-price').text

    if price:
        data['Price'].append(price)
    else:
        data['Price'].append('N/A')




# Store data to csv with pandas
df = pd.DataFrame(data, columns=['Title','Price']) # taking in a dict or multi dimensional array. dict keys match with columns param

# change the range from 0-9, to 1-10. df.index is a range
df.index = df.index + 1
print(df)

# one liner for writing a csv file
df.to_csv('craigslist_postings_file.csv', sep=',', index=False, encoding='utf-8')


print("Code Completed")


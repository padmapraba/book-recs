import  requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import urllib.request


# uing requests to get the document behind the url
BASE_URL = 'https://www.goodreads.com'
# LIST_URL = 'https://www.goodreads.com/list/show/264.Books_That_Everyone_Should_Read_At_Least_Once'
# LIST_URL = 'https://www.goodreads.com/list/show/1043.Books_That_Should_Be_Made_Into_Movies'
LIST_URL = 'https://www.goodreads.com/list/show/10762.Best_Book_Boyfriends'
num_pages = 100

# page = requests.get(URL)
# soup = BeautifulSoup(page.content, 'html.parser')
# print(soup.prettify())
books = {'URL':[]}

for i in range(1,num_pages):
    print(f'Reading page {i}...')
    time.sleep(60)
    list_page_url = f'{LIST_URL}?page={i}'
    list_page = requests.get(list_page_url)
    list_soup = BeautifulSoup(list_page.content, 'html.parser')
    book_table = list_soup.find(
        'table', attrs={'class': 'tableList js-dataTooltip'})
    rows = book_table.find_all('tr')
    books['URL'] += [BASE_URL +
                     r.find('a', attrs={'class': 'bookTitle'}).attrs['href'] for r in rows]

books_df = pd.DataFrame.from_dict(books)
print(books_df)
books_df.to_csv(
    '/Users/padmaprabagaran/dev/book-recs/data/scraped_data7.csv')
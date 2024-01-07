import pandas as pd
import os
import asyncio
import aiohttp
import numpy as np
from bs4 import BeautifulSoup

# Define your column names for the DataFrame
column_names = [
    'image_url', 'book_title', 'book_authors', 'book_rating', 'book_rating_count', 'book_review_count',
 'book_desc',  'genres'
]

# Ensure the CSV file exists with the specified columns
csv_path = '/Users/padmaprabagaran/dev/book-recs/data/data3.csv'
if not os.path.exists(csv_path):
    pd.DataFrame(columns=column_names).to_csv(csv_path, index=False)

# Read the book URLs from a CSV file
books = pd.read_csv('/Users/padmaprabagaran/dev/book-recs/data/book_urls.csv')

async def fetch_book_data(session, url):
    async with session.get(url) as response:
        if response.status == 200:
            book_soup = BeautifulSoup(await response.text(), 'html.parser')
            book = {}
            try:
            # Extract book data similar to your existing code 
                image_url = book_soup.find('img', class_='ResponsiveImage')
                if image_url:
                    book['image_url'] = image_url.get('src')
                else:
                    book['image_url'] = np.nan

                # Title of the book
                book_title = book_soup.find('h1', {'class': 'Text Text__title1', 'data-testid': 'bookTitle', 'aria-label': True})
                if book_title:
                    book['book_title'] = book_title.get_text()
                else:
                    book['book_title'] = np.nan

                # print(i, book['book_title'])

                # Author(s) of the book
                book_author = book_soup.find('span', {'class': 'ContributorLink__name', 'data-testid': 'name'})
                if book_author:
                    book['book_authors'] = book_author.get_text()
                else:
                    book['book_authors'] = np.nan
            

                # Rating given by users on goodreads
                book_rating = book_soup.find('div', {'class': 'RatingStatistics__rating', 'aria-hidden': 'true'})
                if book_rating:
                    book['book_rating'] = book_rating.text.replace('\n', '').strip()
                else:
                    book['book_rating'] = np.nan
                
                # # Rating Count
                rating_count_span = book_soup.find('span', {'data-testid': 'ratingsCount', 'aria-hidden': 'true'})
                if rating_count_span:
                    book['book_rating_count'] = rating_count_span.text.split()[0]  # 
                else:
                    book['book_rating_count'] = np.nan
        

                # No. of reviews for the book
                review_count = book_soup.find('span', {'data-testid': 'reviewsCount', 'aria-hidden': 'true'})
                if review_count:
                    reviews_text = review_count.text
                    reviews_count = reviews_text.split('reviews')[0].strip().replace(',', '')
                    book['book_review_count'] = reviews_count
                else:
                    book['book_review_count'] = np.nan
                
                # A short description of the book, usually found on the back or inside cover of the book. Also called a blurb
                book_desc = book_soup.find('span', class_='Formatted')
                if book_desc:
                    book['book_desc'] = book_desc.text.strip()
                else:
                    book['book_desc'] = np.nan

                # # Format of the book, e.g, paperback, hardcover, Kindle edition, etc.
                # book_format = book_soup.find('div', attrs={'id': 'details'}).find(
                #     'span', attrs={'itemprop': 'bookFormat'})
                # if book_format:
                #     book['book_format'] = book_format.text
                # else:
                #     book['book_format'] = ''

                # # Edition of the book
                # book_edition = book_soup.find('div', attrs={'id': 'details'}).find(
                #     'span', attrs={'itemprop': 'bookEdition'})
                # if book_edition:
                #     book['book_edition'] = book_edition.text
                # else:
                #     book['book_edition'] = ''

                # # No. of pages in the book
                # book_pages = book_soup.find('div', attrs={'id': 'details'}).find(
                #     'span', attrs={'itemprop': 'numberOfPages'})
                # if book_pages:
                #     book['book_pages'] = book_pages.text
                # else:
                #     book['book_pages'] = ''

                # # ISBN code of the book
                # book_isbn = book_soup.find('div', attrs={'id': 'bookDataBox'}).find(
                #     'span', attrs={'itemprop': 'isbn'})
                # if book_isbn:
                #     book['book_isbn'] = book_isbn.text
                # else:
                #     book['book_isbn'] = ''

                # List of genres that the book belongs to. User supplied data.
                genres_ul = book_soup.find('ul', class_='CollapsableList')
                if genres_ul:
                    genre_links = genres_ul.find_all('a')
                    genres_list = [link.text.strip() for link in genre_links]
                    book['genres'] = genres_list
                else:
                    book['genres'] = np.nan


                
                return book  # Return the scraped book data
            except Exception as e:
                # Handle the case where the element is not found
                print(f"Error extracting data for {url}: {e}")
                book = {}
                book['genres'] = np.nan
                book['book_desc'] = np.nan
                book['book_review_count'] = np.nan
                book['book_desc'] = np.nan
                book['book_authors'] = np.nan
                book['book_rating'] = np.nan
                book['book_rating_count'] = np.nan
                book['book_title'] = np.nan
                book['image_url'] = np.nan
                return book

async def main():
    async with aiohttp.ClientSession() as session:
        tasks = []
        save_every = 1
        book_rows = []
        processed_urls = 0  # Counter to track processed URLs

        for i in range(11470,len(books)):
            book_URL = books.at[i, 'URL']
            tasks.append(fetch_book_data(session, book_URL))
            processed_urls += 1

            if len(tasks) == save_every or i == len(books) - 1:
                results = await asyncio.gather(*tasks)
                book_rows.extend(results)
                # print(book_rows)

                # Append the scraped data to the CSV file
                # print(book_rows)
                if book_rows is None:
                    continue
                else:
                    pd.DataFrame(book_rows).to_csv(csv_path, mode='a', header=False, index=False)
                book_rows = []
                tasks = []
                print(f"{processed_urls} URLs processed.")

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    

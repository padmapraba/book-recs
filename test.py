import  requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import urllib.request


# uing requests to get the document behind the url
BASE_URL = 'https://www.goodreads.com'
URL = 'https://www.goodreads.com/book/show/2657.To_Kill_a_Mockingbird'

page = requests.get(URL)
soup = BeautifulSoup(page.content, 'html.parser')
# print(soup.prettify())

# Book Title
book_title = soup.find('h1', {'class': 'Text Text__title1', 'data-testid': 'bookTitle', 'aria-label': True})
if book_title:
    title_text = book_title.get_text()
    print("Book Title:", title_text)
else:
    print("Book title information not found.")

# Authors
author_span = soup.find('span', {'class': 'ContributorLink__name', 'data-testid': 'name'})
if author_span:
    author_name = author_span.get_text()
    print("Author:", author_name)
else:
    print("Author information not found.")

# Ratings
rating_div = soup.find('div', {'class': 'RatingStatistics__rating', 'aria-hidden': 'true'})
if rating_div:
    rating = rating_div.text
    print("Rating:", rating)
else:
    print("Rating information not found.")

rating_count_span = soup.find('span', {'data-testid': 'ratingsCount', 'aria-hidden': 'true'})

# Rating COunts
if rating_count_span:
    rating_count = rating_count_span.text.split()[0]  # Extract the count part before 'ratings'
    print("Rating Count:", rating_count)
else:
    print("Rating count information not found.")

# Review Counts
reviews_count_span = soup.find('span', {'data-testid': 'reviewsCount', 'aria-hidden': 'true'})
if reviews_count_span:
    # Get the text content and split it to extract the reviews count
    reviews_text = reviews_count_span.text
    reviews_count = reviews_text.split('reviews')[0].strip().replace(',', '')  # Extract the count part and remove commas
    print("Number of Reviews:", reviews_count)
else:
    print("Reviews count information not found.")

# Book description
description_span = soup.find('span', class_='Formatted')
if description_span:
    book_description = description_span.text.strip()
    print("Book Description:", book_description)
else:
    print("Book description information not found.")

# Genres
genres_ul = soup.find('ul', class_='CollapsableList')
if genres_ul:
    genre_links = genres_ul.find_all('a')
    genres_list = [link.text.strip() for link in genre_links]
    print("Genres:", genres_list)
else:
    print("Genres information not found.")

# Imagre URL
book_cover_img = soup.find('img', class_='ResponsiveImage')

if book_cover_img:
    # Extract the image URL from the 'src' attribute
    image_url = book_cover_img.get('src')
    print("Image URL:", image_url)
else:
    print("Book cover image not found.")

# Enjoyed books
# enjoyed_books = soup.find('div', class_='CarouselGroup')
# if enjoyed_books:
#     book_links = enjoyed_books.find_all('a', class_='BookCard__clickCardTarget')
#     book_titles = [link.find('div', class_='BookCard__title').text for link in book_links]
#     print("Also enjoyed:", book_titles)
# else:
#     print("Also enjoyed information not found.")



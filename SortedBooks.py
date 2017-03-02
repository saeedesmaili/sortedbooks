from bs4 import BeautifulSoup
from goodreads import client
from operators import itemgetter
import requests
import urllib.request

'''
Add your Goodreads developer keys.
Generate your developer keys here:
https://www.goodreads.com/api/keys
'''
key = 'YOURKEY'
secret = 'YOURSECRET'

'''
Save your books list from https://play.google.com/books as a books.htm in
   the same direcory as this python file
This snippet of code, scraps books list and stores them in a python list
'''
soup = BeautifulSoup(open('books.htm'), 'html.parser')
books = []
for book in soup.findAll('div', {'class': 'bfe-card-details-container'}):
    books.append(str(book.div.a.string))

# some cleanings
books = [b.replace('.epub', '') for b in books]
books = [b.replace('.pdf', '') for b in books]
books = [b.replace('-', ' ') for b in books]
books = [b.replace('_', ' ') for b in books]
books = [b.replace(' ', '+') for b in books]

# Getting exact title and rating of books from Goodreads
def book_search(q, page=1, search_field='all'):
    auth_client = client.GoodreadsClient(key, secret)
    books_list = auth_client.search_books(str(q), page, search_field)
    return books_list[0].title, books_list[0].average_rating

ratings = []
for book in books:
    try:
        print(book)
        ratings.append(book_search(book))
        print(book_search(book))
        print('-----')
    except:
        print('error!')
        continue

# Sorting books by rating
ratings.sort(key=itemgetter(1), reverse=True)

# Exporting sorted list in a CSV file
with open('output.csv', 'w') as f:
    wr = csv.writer(f)
    wr.writerows(ratings)

print(ratings)

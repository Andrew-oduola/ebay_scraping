import requests 
from bs4 import BeautifulSoup




page = 1
page_link = 'https://books.toscrape.com/catalogue/page-1.html'

while page <= 50:
    response = requests.get(page_link)
    if response.status_code == 200:
        count = 0
        soup = BeautifulSoup(response.text, 'html.parser')
        books = soup.find_all('h3')
        # print(books)
        for book in books:
            count += 1
            book_url = 'https://books.toscrape.com/catalogue/' + book.find('a')['href']
            # print(book, book_url)
            book_response = requests.get(book_url)
            if book_response.status_code == 200:
                book_soup = BeautifulSoup(book_response.text, 'html.parser')
                book_title = book_soup.find('h1').get_text()
                book_price = book_soup.find('p', class_='price_color').get_text()
                book_description = book_soup.find_all('p')[3].get_text(strip=True)
                print(f"Title: {book_title}, Price: {book_price}, Description: {book_description}")
            else:
                print(f"Error with book {book.get_text('title')}'s status code: {book_response.status_code}")

        print(f"Total book {count}")
    else:
        print(f"Error with the status code: {response.status_code}")
    page += 1
    page_link = 'https://books.toscrape.com/catalogue/page-' + str(page) + '.html'
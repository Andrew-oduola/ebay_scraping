import requests
from bs4 import BeautifulSoup
from pprint import pprint

url = 'https://www.ebay.com/b/Sports-Memorabilia-Fan-Shop-Sports-Cards/64482/bn_1857919'

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Referer": "https://www.ebay.com/"
}


response = requests.get(url, headers=headers)
try:
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        # Example: Find product names
        products = soup.find(class_='textual-display bsig__title__text')
        product_names = [product.get_text(strip=True) for product in products]

        pprint(product_names)
    else:
        print(f"Failed to fetch {url}: Status code {response.status_code}")
except requests.exceptions.RequestException as e:
    print(f"Error for {url}: {e}")






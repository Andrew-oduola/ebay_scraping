import requests
from bs4 import BeautifulSoup
from pprint import pprint

# URL of the Amazon product listing page
# url = "https://www.amazon.com/s?k=laptops"
url = "https://www.amazon.com/s/ref=nb_sb_noss?url=search-alias%3Darts-crafts-intl-ship&field-keywords=&crid=31U4YIQ6D5EFN&sprefix=%2Carts-crafts-intl-ship%2C264"

# Headers to mimic a browser request
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
}

# Send the request
response = requests.get(url, headers=headers)

if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Find product containers (Amazon changes these classes often; inspect the page to confirm)
    # products = soup.find_all("div", class_="s-main-slot s-result-list s-search-results sg-row")
    products  = soup.find_all("div", class_="a-section a-spacing-small a-spacing-top-small")
    # product_headers = soup.find_all("h2", class_="a-size-medium a-spacing-none a-color-base a-text-normal")
    product_headers = soup.find_all("div", class_="a-section a-spacing-small puis-padding-left-small puis-padding-right-small")
    pprint(product_headers)
    product_list = []
    for product in product_headers:
        # Extract product name
        name = product.find("span")
        name = name.get_text(strip=True) if name else "N/A"

        # Extract product price
        price_whole = product.find("span", class_="a-price-whole")
        price_fraction = product.find("span", class_="a-price-fraction")
        price = (
            f"{price_whole.get_text(strip=True)}.{price_fraction.get_text(strip=True)}"
            if price_whole and price_fraction
            else "N/A"
        )

        # Extract product rating
        rating = product.find("span", class_="a-icon-alt")
        rating = rating.get_text(strip=True) if rating else "N/A"

        # Append details to the list
        product_list.append({"Name": name, "Price": price, "Rating": rating})

    # Print the results
    pprint(product_list)
else:
    print(f"Failed to fetch the webpage. Status code: {response.status_code}")

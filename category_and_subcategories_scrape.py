import requests
from bs4 import BeautifulSoup
import pandas as pd

url = "https://www.ebay.com/n/all-categories"

# Send a request to the website
response = requests.get(url)
if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')
else:
    print(f"Failed to fetch the webpage. Status code: {response.status_code}")
    exit()

categories = soup.find_all(class_='ttl')
category_names = [category.get_text(strip=True) for category in categories]

subcategory_links = soup.find_all(class_='cat-url')
subcategory_names = [subcategory.get_text(strip=True) for subcategory in subcategory_links]
subcategory_urls = [subcategory['href'] for subcategory in subcategory_links]

all_products = []

for category_name in category_names:
    print(f"Processing category: {category_name}")
    for subcategory_name, subcategory_url in zip(subcategory_names, subcategory_urls):
        print(f"  Scraping subcategory: {subcategory_name}")
        try:
            # Fetch the subcategory page
            sub_response = requests.get(subcategory_url)
            if sub_response.status_code == 200:
                sub_soup = BeautifulSoup(sub_response.text, 'html.parser')
                products = sub_soup.find_all(class_='textual-display')
                product_names = [product.get_text(strip=True) for product in products]

                # Add the products to the list
                for product_name in product_names:
                    all_products.append({
                        "Category": category_name,
                        "Subcategory": subcategory_name,
                        "Product Name": product_name
                    })
            else:
                print(f"Status code: {sub_response.status_code}")
                print(f"Failed to fetch the subcategory page: {subcategory_url}")
        except Exception as e:
            print(f"An error occurred while scraping {subcategory_name}: {e}")

product_df = pd.DataFrame(all_products)

output_file = "ebay_products_with_categories.xlsx"
product_df.to_excel(output_file, index=False)

print(f"Product data saved to {output_file}")

import requests
from bs4 import BeautifulSoup

# Fungsi untuk mengumpulkan informasi produk dari Amazon berdasarkan ASIN
def scrape_amazon(asin):
    product_link = f"https://www.amazon.com/dp/{asin}"

    # Mengirim permintaan HTTP ke URL produk
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
        'Accept-Language': 'en-US,en;q=0.9',
        'Referer': 'https://www.google.com/'
    }

    response = requests.get(product_link, headers=headers)

    # Memeriksa status respons
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')

        # Mengumpulkan informasi produk
        product_name = soup.select_one('#productTitle').get_text().strip()
        product_image = soup.select_one('#landingImage')['src']
        product_price = get_product_price(soup)
        product_description, additional_description = get_product_description(soup)

        return {
            'name': product_name,
            'image': product_image,
            'price': product_price,
            'description': product_description,
            'additional_description': additional_description
        }
    else:
        print(f"Failed to retrieve the page for product URL: {product_link}. Status code: {response.status_code}")
        return None

# Fungsi untuk mengumpulkan harga produk
def get_product_price(soup):
    price_whole = soup.select_one('.a-price-whole')
    price_fraction = soup.select_one('.a-price-fraction')
    if price_whole and price_fraction:
        return f"${price_whole.text.strip()}.{price_fraction.text.strip()}"
    elif price_whole:
        return f"${price_whole.text.strip()}"
    return "Price Not Available"

# Fungsi untuk mengumpulkan deskripsi produk
def get_product_description(soup):
    description = soup.select_one('#feature-bullets')
    additional_description = soup.select_one('#productDescription')

    product_description_items = []
    additional_description_text = ""

    if description:
        product_description_items.extend([li.text.strip() for li in description.select('li') if li.text.strip()])
    if additional_description:
        additional_description_text = additional_description.get_text(separator=" ").strip()

    product_description = '\n'.join(product_description_items)
    return product_description, additional_description_text
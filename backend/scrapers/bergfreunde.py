import requests
from bs4 import BeautifulSoup

def get_price():
    url = "https://www.bergfreunde.nl/tenaya-indalo-klimschoenen/?aid=6e824d326b73d7b3ceccfc29515ebf76&pid=10004&bfgb=false"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find the product title
    title_tag = soup.find("span", class_="product-title")
    title = title_tag.get_text(strip=True) if title_tag else "Unknown Title"

    # Find the price
    price_tags = soup.find_all("span", class_="js-fprice")

    for i, tag in enumerate(price_tags):

        parent = tag.find_parent()
        if 'js-price' in parent.get("class"):
            current_price = tag.text.strip()
            print(f"Final price {i + 1}: {current_price}")


    return {
        "title": title,
        "price": current_price,
        "url": url
    }
if __name__ == "__main__":
    print(get_price())



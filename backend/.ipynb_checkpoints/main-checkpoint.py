from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import json
import os
from datetime import datetime
from scrapers.bergfreunde import get_price

app = FastAPI()

# Allow frontend (e.g., GitHub Pages) to fetch from this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # allow your frontend dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

PRICES_FILE = "prices.json"

# Load stored prices or initialize
def load_prices():
    if not os.path.exists(PRICES_FILE):
        return {}
    with open(PRICES_FILE, "r") as f:
        return json.load(f)

def save_prices(prices):
    with open(PRICES_FILE, "w") as f:
        json.dump(prices, f, indent=2)

@app.get("/products")
def get_products():
    current = get_price()
    current_price = current["price"]
    now = datetime.now().isoformat()

    prices = load_prices()
    product_key = "bergfreunde"

    previous = prices.get(product_key, {})
    previous_price = previous.get("price", current_price)

    dropped = current_price < previous_price

    # Save updated price
    prices[product_key] = {
        "price": current_price,
        "last_checked": now
    }
    save_prices(prices)

    return [{
        "name": current["title"],
        "url": current["url"],
        "price": current_price,
        "previous_price": previous_price,
        "dropped": dropped,
        "last_checked": now
    }]
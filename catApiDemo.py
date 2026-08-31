import requests
from PIL import Image
import io
import matplotlib.pyplot as plt

API_KEY = "live_GBkBNHJZzsBFsfGTBmSHM9St7FE7WbeaP9HJwdnQjU3IICd9YV7HfihTTqCZu3uI"
BASE_URL = "https://api.thecatapi.com/v1"

def get_random_cat_with_info():
    """fetch random cat image with breed info"""
    url = f"{BASE_URL}/images/search"
    params = {
        "limit":1,
        "has_breeds":1,}
    headers = {"x-api-key": API_KEY} if API_KEY else {}
    print("Headers being sent:", headers)
    response = requests.get(url, params=params, headers=headers)
    response.raise_for_status()

    print("Status code:", response.status_code)
    print("Rate limit remaining:", response.headers.get("x-ratelimit-remaining"))
    data = response.json()[0]
    print("Raw data:", data)

    info = {
        "url": data["url"],
        "width": data.get("width"),
        "height": data.get("height"),
    }

    if data.get("breeds"):
        breed = data["breeds"][0]
        info.update({
            "name": breed.get("name"),
            "origin": breed.get("origin"),
            "temperament": breed.get("temperament"),
            "description": breed.get("description"),
            "life_span": breed.get("life_span"),
            "wikipedia_url": breed.get("wikipedia_url"),
        })
    else:
        info["name"] = "Unknown breed"
    return info
def display_cat(info):
    """download image and display with info"""
    img_data = requests.get(info["url"]).content
    img = Image.open(io.BytesIO(img_data))

    plt.figure(figsize=(6,6))
    plt.imshow(img)
    plt.axis("off")
    plt.title(info["name"], fontsize=14, fontweight="bold")
    plt.figtext(.0, .01,
                f"Origin: {info.get('origin', 'N/A')} | Life Span: {info.get('life_span', 'N/A')} yrs",
                ha="center", fontsize=9, wrap=True)
    plt.tight_layout()
    plt.show()

    print(f"\n{'='*50}")
    print(f"Breed: {info['name']}")
    print(f"Origin: {info['origin']}")
    print(f"Temperament: {info['temperament']}")
    print(f"Description: {info['description']}")
    print(f"Life span: {info['life_span']}")
    print(f"More info: {info["wikipedia_url"]}")
    print(f"{'='*50}\n")

if __name__ == "__main__":
    cat_info = get_random_cat_with_info()
    display_cat(cat_info)

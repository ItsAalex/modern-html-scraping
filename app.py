# HTTP client that's used for making requests to the web server
import httpx

from selectolax.parser import HTMLParser

# Module for creating data classes(used for storing data in a structured way)
from dataclasses import dataclass

# Module for parsing URLs
# urljoin is used for combining base URL and relative URL into an absolute URL
from urllib.parse import urljoin

# Library for rich text and beautiful formatting in the terminal
from rich import print


# Model for our data
@dataclass
class Product:
    name: str
    sku: str
    price: str
    rating: str

@dataclass
class Response:
    # can be queried with CSS selectors
    body_html: HTMLParser
    # next page link is href and it is attribute
    next_page: dict

def get_page(client, url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
     }
    resp = client.get(url, headers=headers)
    html = HTMLParser(resp.text)

    if html.css_first("a[data-id=pagination-test-link-next]"):
        next_page = html.css_first("a[data-id=pagination-test-link-next]").attributes
    else:
        next_page = {"href": None}

    return Response(body_html=html, next_page=next_page)

def main():
    client = httpx.Client()
    url = "https://www.rei.com/c/backpacks?page=25"

    print(get_page(client, url))

if __name__ == "__main__":
    main()
import requests
from bs4 import BeautifulSoup

def scrape_bing(query):
    url = f"https://www.bing.com/search?q={query}"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    links = []
    for result in soup.find_all('a', href=True):
        if "http" in result['href']:
            links.append(result['href'])

    return links

print(scrape_bing('python programming'))
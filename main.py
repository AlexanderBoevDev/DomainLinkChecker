import requests
from bs4 import BeautifulSoup
from yandex_auth import get_access_token
import pandas as pd

def fetch_links_from_domain(domain):
    """ Fetch all URLs from a given domain using BeautifulSoup """
    try:
        response = requests.get(domain)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        links = set(a['href'] for a in soup.find_all('a', href=True) if a['href'].startswith('http'))
        return links
    except requests.RequestException as e:
        print(f"Ошибка запроса: {e}")
        return set()

def fetch_yandex_webmaster_links(access_token):
    """ Fetch URLs from Yandex Webmaster using the API """
    headers = {
        "Authorization": f"OAuth {access_token}"
    }
    # URL to fetch the links from Yandex Webmaster; you need to adjust it according to actual API.
    api_url = "https://api.yandex.com/webmaster/url"
    try:
        response = requests.get(api_url, headers=headers)
        response.raise_for_status()
        data = response.json()
        yandex_links = set(item['url'] for item in data['links'])
        return yandex_links
    except requests.RequestException as e:
        print(f"Ошибка при доступе к API Яндекс Вебмастера: {e}")
        return set()

def compare_links(domain_links, yandex_links):
    """ Compare domain links with Yandex Webmaster links and find missing """
    domain_links_df = pd.Series(list(domain_links))
    yandex_links_df = pd.Series(list(yandex_links))
    return domain_links_df[~domain_links_df.isin(yandex_links_df)]

if __name__ == "__main__":
    domain = 'https://example.com'
    access_token = get_access_token()
    domain_links = fetch_links_from_domain(domain)
    yandex_links = fetch_yandex_webmaster_links(access_token)
    missing_links = compare_links(domain_links, yandex_links)
    print("Ссылки, отсутствующие в Яндекс Вебмастере:", missing_links.tolist())

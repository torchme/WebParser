import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

def parse_page(vacancy_name='data analytics'):
    """
    Parse the given page URL using proxies and raise an exception if the request fails.

    Parameters
    ----------
    url : str
        The URL of the page to parse.
    """
    payload = {
        'search_period': 14,
        'text': vacancy_name,
        'ored_clusters': True,
        'enable_snippets': True,
        'clusters': True,
        'area': 113,  # 113 - Russia
        'hhtmFrom': 'vacancy_search_catalog',
    }
    sessia = requests.Session()
    try:
        req = sessia.get(f'https://hh.ru/search/vacancy?text={vacancy_name}&area={113}&page={0}', headers={'User-Agent': 'Custom'}, data=payload)
        if req.status_code == requests.codes.ok:
            soup = BeautifulSoup(req.text, "html.parser")
        num_vacancy = soup.find('h1', {'class': 'bloko-header-section-3'}).text
        num_vacancy = int(''.join(c for c in num_vacancy if c.isdigit()))
        num_page = num_vacancy // 50 + 1

        total_links = []
        for no_page in range(0, num_page):
            req = requests.get(f'https://hh.ru/search/vacancy?text={vacancy_name}&area={113}&page={no_page}', headers={'User-Agent': 'Custom'}, data=payload)
            if req.status_code == requests.codes.ok:
                soup = BeautifulSoup(req.text, "html.parser")
                links_vacancys = soup.find_all('a', {'class': 'serp-item__title'})
                links_vacancys = [link.get('href') for link in links_vacancys]
                total_links.extend(links_vacancys)
        df = pd.DataFrame(total_links, columns=['Links'])
        df.to_excel(f'data/links_{time.time.now()}.xlsx', index=False)

    except Exception as e:
        print(e)


if __name__ == '__main__':
    parse_page(vacancy_name='data science')
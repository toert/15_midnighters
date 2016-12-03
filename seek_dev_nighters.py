import requests
import pytz
import datetime

URL = 'https://devman.org/api/challenges/solution_attempts/?page='


def request_API_page(number_of_page):
    URL_of_page = '{}{}'.format(URL, str(number_of_page))
    return requests.get(URL_of_page)


def get_count_of_pages():
    for page in range(1,100):
        request = request_API_page(page)
        if request.status_code == 404:
            return page-1


def load_attempts(pages):
    for page in range(1, pages):
        response = request_API_page(page).json()
        #print(json.dumps(response, indent=4, sort_keys=True, ensure_ascii=False))
        for record in response['records']:
            yield {
                'username': record['username'],
                'timestamp': record['timestamp'],
                'timezone': record['timezone'],
            }

def get_midnighters(records):
    pass

if __name__ == '__main__':
    pages_count = get_count_of_pages()
    records = list(load_attempts(pages_count))

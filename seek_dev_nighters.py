import requests
from pytz import timezone
from datetime import datetime


URL = 'https://devman.org/api/challenges/solution_attempts/?page='
START_NIGHT = 0
END_NIGHT = 6
FIRST_PAGE_NUMBER = 1


def request_api_page(number_of_page):
    url_of_page = '{}{}'.format(URL, str(number_of_page))
    return requests.get(url_of_page)


def get_count_of_pages():
    request = request_api_page(FIRST_PAGE_NUMBER).json()
    return request['number_of_pages']


def load_attempts(pages):
    for page in range(FIRST_PAGE_NUMBER, pages):
        response = request_api_page(page).json()
        for record in response['records']:
            yield {
                'username': record['username'],
                'timestamp': record['timestamp'],
                'timezone': record['timezone'],
            }


def get_midnighters(records):
    midnighters = []
    for record in records:
        time = datetime.fromtimestamp(record['timestamp'],
                                      timezone(record['timezone']))
        hour = datetime.timetuple(time)[3]
        if hour in range(START_NIGHT, END_NIGHT) and\
                        record['username'] not in midnighters:
            midnighters.append(record['username'])
    return midnighters


def print_midnighters(midnighters):
    print('\"Don\'t want to sleep after 24:00 PM\" guys are:')
    for sleepman in midnighters:
        print(sleepman)


if __name__ == '__main__':
    pages_count = get_count_of_pages()
    records = list(load_attempts(pages_count))
    records = list(filter(lambda record: record['timestamp'] is not None, records))
    print_midnighters(get_midnighters(records))
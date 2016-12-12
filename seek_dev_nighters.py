import requests
from pytz import timezone
from datetime import datetime


URL = 'https://devman.org/api/challenges/solution_attempts/'
START_NIGHT = 0
END_NIGHT = 6
FIRST_PAGE_NUMBER = 1


def request_api_page(number_of_page):
    payload = {'page': number_of_page}
    return requests.get(URL, params=payload)


def load_attempts():
    page = FIRST_PAGE_NUMBER
    while True:
        response = request_api_page(page).json()
        page += 1
        pages = response['number_of_pages']
        for record in response['records']:
            yield {
                'username': record['username'],
                'timestamp': record['timestamp'],
                'timezone': record['timezone'],
            }
        if page > pages:
            break


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
    records = load_attempts()
    records = list(filter(lambda record: record['timestamp'] is not None, records))
    print_midnighters(get_midnighters(records))
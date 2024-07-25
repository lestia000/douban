import random
import time
import requests


def get_page(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:125.0) Gecko/20100101 Firefox/125.0'
    }
    retries = 5
    retry_delay = random.randint(1, 3)
    for retry in range(retries):
        try:
            response = requests.get(url, headers=headers, timeout=.5)
            if response.status_code == 200:
                return response.text
            else:
                raise requests.exceptions.RequestException
        except Exception as e:
            print("reconnecting...")
            if retry == retries - 1:
                raise e
            time.sleep(retry_delay)

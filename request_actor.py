import requests
# import json
# from requests.auth import HTTPBasicAuth
# from requests import Session
# from fastapi import FastAPI
import os
import time

class GRequest():
    def __init__(self):
        self.BEARER_KEY = os.getenv('GITHUB_BEARER_KEY')
        self.GITHUB_GRAPHQL_ENDPOINT = 'https://api.github.com/graphql'
        self.GITHUB_GRAPHQL_HEADERS = {'Authorization': f'Bearer {self.BEARER_KEY}'}

        self.GITHUB_REST_ENDPOINT = 'https://api.github.com'
        self.GITHUB_REST_HEADERS = {
            'Accept': 'application/vnd.github+json',
            'X-GitHub-Api-Version': '2022-11-28',
            'Authorization': f'Bearer {self.BEARER_KEY}'
        }
    def github_post_graphql_request(self, _query, variables = None):
        print(f'[+] Fetching data from the url: {self.GITHUB_GRAPHQL_ENDPOINT}')
        session = requests.Session()
        session.headers.update(self.GITHUB_GRAPHQL_HEADERS)
        response = session.post(self.GITHUB_GRAPHQL_ENDPOINT, json={'query': _query, 'variables': variables})

        if response.status_code in (301, 302):
            response = session.post(response.headers['location'], json={'query': _query, 'variables': variables})
        
        if response.status_code != 200:
            print(f" [-] Failed to retrieve from API. Status code: {response.status_code}")
            return None

        print('[+] Done fetching data\n')
        return response.json()


    def github_post_rest_request(self, url, variables = None, max_page_fetch = float('inf')):

        url = f"{self.GITHUB_REST_ENDPOINT}{url}"
        result = []

        current_fetch_count = 0
        print(f'[+] Fetching data from the url: {url}')
        while url and (current_fetch_count < max_page_fetch):
            print(f' [.] Fetching page {current_fetch_count + 1} - {url}')
            session = requests.Session()
            session.headers.update(self.GITHUB_REST_HEADERS)
            response = session.get(url, params=variables)
            if response.status_code == 202:
                time.sleep(1)
                print(' [.] Waiting for the data to be ready...')
                continue # fetch again!

            elif response.status_code != 200:
                print(f" [-] Failed to retrieve from API. Status code: {response.status_code}")
                return None
            
            url = response.links.get("next", {}).get("url", None)
            if max_page_fetch == 1 or url is None:
                return response.json()
            
            result.extend(response.json())
            current_fetch_count += 1

        print('[+] Done fetching data\n')
        return result



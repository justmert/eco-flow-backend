import requests
# import json
# from requests.auth import HTTPBasicAuth
# from requests import Session
# from fastapi import FastAPI
import os
import time

class GithubRequest():
    def __init__(self):
        self.BEARER_KEY = os.getenv('GITHUB_BEARER_KEY')
        self.GRAPHQL_ENDPOINT = 'https://api.github.com/graphql'
        self.GRAPHQL_HEADERS = {'Authorization': f'Bearer {self.BEARER_KEY}'}

        self.REST_ENDPOINT = 'https://api.github.com'
        self.REST_HEADERS = {
            'Accept': 'application/vnd.github+json',
            'X-GitHub-Api-Version': '2022-11-28',
            'Authorization': f'Bearer {self.BEARER_KEY}'
        }
    def post_query(self, _query, variables = None):
        print('[+] Fetching data from the url: ', self.GRAPHQL_ENDPOINT)
        session = requests.Session()
        session.headers.update(self.GRAPHQL_HEADERS)
        response = session.post(self.GRAPHQL_ENDPOINT, json={'query': _query, 'variables': variables})
        if response.status_code in (301, 302):
            response = session.post(response.headers['location'], json={'query': _query, 'variables': variables})
        
        if response.status_code != 200:
            print(f" [-] Failed to retrieve from API. Status code: {response.status_code}")
            return None

        print('[+] Done fetching data\n')
        return response.json()

    def post_rest(self, url, variables = None, fetch_all = False, max_fetch = -1):
        if fetch_all and max_fetch != -1:
            print('[-] Cannot fetch all and limit the number of fetches at the same time')
            return None

        url = f"{self.REST_ENDPOINT}{url}"
        result = []
        current_fetch = 0
        print('[+] Fetching data from the url: ', url)
        while url and (max_fetch == -1 or current_fetch < max_fetch):
            session = requests.Session()
            session.headers.update(self.REST_HEADERS)
            response = session.get(url, params=variables)
            if response.status_code == 202:
                time.sleep(0.5)
                print(' [.] Waiting for the data to be ready...')
                continue # fetch again!

            elif response.status_code != 200:
                print(f" [-] Failed to retrieve from API. Status code: {response.status_code}")
                return None
                
            if not fetch_all and max_fetch == -1:
                result = response.json()
                break

            result.extend(response.json())
            url = response.links.get("next", {}).get("url", None)
            current_fetch += 1
        print('[+] Done fetching data\n')
        return result

    def get_owner_and_repo(self, repo):
        return repo.split('/')




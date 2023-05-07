import requests
# import json
# from requests.auth import HTTPBasicAuth
# from requests import Session
# from fastapi import FastAPI
import os
import time
from time import sleep
import datetime

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

        elif response.status_code == 403:
            print(f"Rate limit exceeded. Sleeping for 1 hour.")
            self.sleep_rate_limiting()
            return self.github_post_graphql_request(_query, variables)

        print('[+] Done fetching data\n')
        return response.json()

    def sleep_rate_limiting(self):
        # Get the current time
        now = datetime.datetime.now()
        
        # Calculate the number of seconds remaining until the start of the next hour
        seconds_to_wait = (60 - now.minute - 1) * 60 + (60 - now.second)

        # Sleep for the calculated number of seconds
        print(f"Sleeping for {seconds_to_wait} seconds")
        time.sleep(seconds_to_wait)

        # After the sleep, the time will be at the start of the next hour
        print("Done sleeping, time is now:", datetime.datetime.now())


    def check_repo(self, owner, repo):
        # Make an HTTP request to the GitHub API endpoint for the repository
        response = requests.get(f"https://api.github.com/repos/{owner}/{repo}")

        # Check if the response is successful or if the repository is inaccessible
        if response.status_code == 200:
            print(f"{repo} is accessible.")
            return True
        # Check if the response is successful or if the repository is inaccessible
        elif response.status_code == 202:
            print(f"{repo} is accessible.")
            return True
        
        elif response.status_code == 404:
            print(f"{repo} does not exist.")
            return False
        elif response.status_code == 401:
            print(f"{repo} is private.")
            return False
        elif response.status_code == 410:
            print(f"{repo} has been deleted.")
            return False
        elif response.status_code == 403:
            print(f"Rate limit exceeded. Sleeping for 1 hour.")
            self.sleep_rate_limiting()
            return True
        else:
            print(f"{repo} ??")
            print(response.status_code)
            print(response.json())
            return False

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
            
            elif response.status_code == 403:
                print(f"Rate limit exceeded. Sleeping for 1 hour.")
                self.sleep_rate_limiting()
                continue

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



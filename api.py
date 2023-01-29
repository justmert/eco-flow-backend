from fastapi import FastAPI
from req import Req
from datetime import datetime
import json
from fetch import Fetch

app = FastAPI()
fetch = Fetch()

@app.get("/hello")
def say_hello():
    return "Hi :)"

@app.get("/code_frequency/{owner}/{repo}")
def get_code_frequency(owner: str, repo: str):
    # print(fetch.get_data)
    # print(fetch.get_data)
    return fetch.get_data[f"{owner}/{repo}"]["code_frequency"]

@app.get("/commit_history/{owner}/{repo}")
def get_commit_history(owner, repo):
    # return None
    return fetch.get_data[f"{owner}/{repo}"]["commit_history"]


@app.get("/issue_activity/{owner}/{repo}")
def get_issue_activity(owner, repo):
    return fetch.get_data[f"{owner}/{repo}"]["issue_activity"]

@app.get("/pull_request_activity/{owner}/{repo}")
def get_pull_request_activity(owner, repo):
    # print(fetch.get_data)
    return fetch.get_data[f"{owner}/{repo}"]["pull_request_activity"]

@app.get("/star_activity/{owner}/{repo}")
def get_pull_request_activity(owner, repo):
    # print(fetch.get_data)
    return fetch.get_data[f"{owner}/{repo}"]["star_activity"]

@app.get("/issue_count/{owner}/{repo}")
def get_issue_count(owner, repo):
    # print(fetch.get_data)
    return fetch.get_data[f"{owner}/{repo}"]["issue_count"]


@app.get("/pull_request_count/{owner}/{repo}")
def get_(owner, repo):
    # print(fetch.get_data)
    return fetch.get_data[f"{owner}/{repo}"]["pull_request_count"]


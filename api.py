from datetime import datetime
import json

# API IS NOT IN USE, CHANGED TO FIREBASE

# from fetch_data import Fetch
# from fastapi import FastAPI
# app = FastAPI()
app = None
fetch = None 

@app.get("/hello")
def say_hello():
    return "Hi :)"

@app.get("/code_frequency/{owner}/{repo}")
def get_code_frequency(owner: str, repo: str):
    return fetch.get_data[f"{owner}/{repo}"].get("code_frequency", None)


@app.get("/commit_history/{owner}/{repo}")
def get_commit_history(owner, repo):
    return fetch.get_data[f"{owner}/{repo}"].get("commit_history", None)


@app.get("/issue_activity/{owner}/{repo}")
def get_issue_activity(owner, repo):
    return fetch.get_data[f"{owner}/{repo}"].get("issue_activity",None)


@app.get("/pull_request_activity/{owner}/{repo}")
def get_pull_request_activity(owner, repo):
    return fetch.get_data[f"{owner}/{repo}"].get("pull_request_activity",None)


@app.get("/star_activity/{owner}/{repo}")
def get_star_activity(owner, repo):
    return fetch.get_data[f"{owner}/{repo}"].get("star_activity",None)


@app.get("/issue_count/{owner}/{repo}")
def get_issue_count(owner, repo):
    return fetch.get_data[f"{owner}/{repo}"].get("issue_count",None)


@app.get("/pull_request_count/{owner}/{repo}")
def get_pull_request_count(owner, repo):
    return fetch.get_data[f"{owner}/{repo}"].get("pull_request_count",None)


@app.get("/top_contributors/{owner}/{repo}")
def get_top_contributors(owner, repo):
    return fetch.get_data[f"{owner}/{repo}"].get("top_contributors",None)


@app.get("/recent_commits/{owner}/{repo}")
def get_recent_commits(owner, repo):
    return fetch.get_data[f"{owner}/{repo}"].get("recent_commits", None)


@app.get("/recent_issues/{owner}/{repo}")
def get_recent_issues(owner, repo):
    return fetch.get_data[f"{owner}/{repo}"].get("recent_issues",None)


@app.get("/repository_info/{owner}/{repo}")
def get_repository_info(owner, repo):
    return fetch.get_data[f"{owner}/{repo}"].get("repository_info",None)

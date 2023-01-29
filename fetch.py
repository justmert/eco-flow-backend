import json
from req import Req
from datetime import datetime
import pandas as pd
from collections import defaultdict
from datetime import datetime, timedelta
import operator


class Fetch:
    def __init__(self):
        self.req = Req()
        self.data = {}
        
        with open("repositories.json", "r") as f:
            self.repositories = json.load(f)['repositories']

        for repository in self.repositories:
            owner = repository['owner']
            repo = repository['repo']
            self.data[self._get_hash(owner, repo)] = {}

        self.fetch()

    def fetch(self):
        for repository in self.repositories:
            owner = repository['owner']
            repo = repository['repo']
            self.commit_history(owner, repo)
            
            self.code_frequency(owner, repo)

            self.issue_count(owner, repo)

            self.issue_activity(owner, repo)
            
            self.pull_request_count(owner, repo)

            self.pull_request_activity(owner, repo)
            print('d')

            self.star_activity(owner, repo)
            print('e')
            
            self.get_top_contributors(owner, repo)
            print('f')

    @property
    def get_data(self):
        return self.data

    def _get_hash(self, owner, repo):
        return f"{owner}/{repo}"


    def commit_history(self, owner, repo):
        # Returns the total commit counts for the owner and total commit counts in all. all is everyone combined, including the owner in the last 52 weeks
        data = self.req.post_rest(f"/repos/{owner}/{repo}/stats/participation")
        if data is None:
            return None

        # Initialize the series data
        series = [
            {"data": data["all"], "type": "line", "smooth": True, "showSymbol": False},
            # {"data": data["owner"], "type": "line", "stack": "owner"}
        ]

        # Define the chart option
        x_range = list(range(len(data["all"])))
        option = {
            "xAxis": {"data": x_range},
            "yAxis": {},
            "series": series,
            "tooltip": {
                "trigger": 'axis',
            },
            "dataZoom": [
                {
                    "type": 'slider',
                    "start": 50,
                    "bottom": 10,
                    # "xAxisIndex": 0,
                    "end": 100
                },
            ],
        }
        self.data[self._get_hash(owner, repo)]['commit_history'] = option


    def code_frequency(self, owner, repo):
        # weekly aggregate of the number of additions and deletions pushed to a repository.
        data = self.req.post_rest(
            f"/repos/{owner}/{repo}/stats/code_frequency")

        if data is None:
            return None

        # Initialize the x-axis labels
        x_axis = []

        # Initialize the series data
        series = [
            {"data": [], "type": "line", "stack": "x", "smooth": True, "showSymbol": False},
            {"data": [], "type": "line", "stack": "x", "smooth": True, "showSymbol": False}
        ]

        # Iterate over the code frequency data
        for item in data:
            # Append the x-axis label
            x_axis.append(datetime.fromtimestamp(item[0]).date())

            # Append the series data
            series[0]["data"].append(item[1])
            series[1]["data"].append(item[2])

        # Define the chart option
        option = {
            "xAxis": {"data": x_axis},
            "yAxis": {},
            "series": series,
            "tooltip": {
                "trigger": 'axis',
            },
            "dataZoom": [
                {
                    "type": 'slider',
                    "start": 50,
                    "bottom": 10,
                    "xAxisIndex": 0,
                    "end": 100
                },
            ],

        }
        print(option)
        self.data[self._get_hash(owner, repo)]['code_frequency'] = option


    def issue_activity(self, owner, repo):
        now = datetime.now()
        since_date = (now - timedelta(days=30)
                      ).date().strftime("%Y-%m-%dT%H:%M:%SZ")

        data = self.req.post_rest(f"/repos/{owner}/{repo}/issues",
                                  {"state": "all", "per_page": 100, "page": 1, "sort": "updated", "direction": "desc"})

        if data is None:
            return None

            # Initialize lists to store the data for the x and y axis
        # x_data = []
        y_data_state = {}

        # Iterate through the issues
        for issue in data:
            is_pull_request = issue.get("pull_request", None)
            if is_pull_request is not None:  # meh, it is pr, skip it
                continue

            # Extract the date when the issues was created
            # created_at = datetime.strptime(pull_request["created_at"], "%Y-%m-%dT%H:%M:%SZ").date()

            # Extract the date when the issues was updated
            updated_at = datetime.strptime(
                issue["updated_at"], "%Y-%m-%dT%H:%M:%SZ").date()

            # Append the date to the x data list
            # x_data.append(updated_at)
            updated_date_exist = y_data_state.get(updated_at, None)
            if updated_date_exist is None:
                y_data_state[updated_at] = {"open": 0, "closed": 0}

            # Check if the issues is open or closed
            if issue["state"] == "open":
                # Increment the count for open issues
                y_data_state[updated_at]["open"] += 1
            else:
                # Increment the count for closed issues
                y_data_state[updated_at]["closed"] += 1

        # print(y_data_state)
        # zipped = zip(y_data_state.keys(), y_data_state.values())
        # zipped = sorted(zipped, key=lambda x: x[0])
        zipped = {k: v for k, v in sorted(y_data_state.items(), key=lambda item: item[0], reverse=False)}

        # Define the option for the stacked bar chart
        option = {
            "xAxis": {
                "data": list(zipped.keys())
            },
            "yAxis": {},
            "series": [
                {
                    "data": [v['open'] for _, v in zipped.items()],
                    "type": "bar",
                    "stack": "issue_activity",
                    "name":"open"
                },
                {
                    "data": [v['closed'] for _, v in zipped.items()],
                    "type": "bar",
                    "stack": "issue_activity",
                    "name":"closed"
                }
            ],
            "tooltip": {
                "trigger": 'axis',
            }
        }
        self.data[self._get_hash(owner, repo)]['issue_activity'] = option


    def issue_count(self, owner, repo ):
        query = """
            query ($owner: String!, $name: String!) {
            repository(owner: $owner, name: $name) {
                    open: issues(states:OPEN) {
						totalCount
					}
					closed: issues(states:CLOSED) {
						totalCount    
                    }
                }
            }        
        """

        variables = {
            "owner": owner,
            "name": repo,
        }

        data = self.req.post_query(query, variables)

        if data is None:
            return None

        
        option = {
            "tooltip": {
                "trigger": 'item'
            },
            "legend": {
                "top": '5%',
                "left": 'center'
            },
            "series": [
                {
                "name": 'Issue Count',
                "type": 'pie',
                "radius": ['40%', '70%'],
                "avoidLabelOverlap": False,
                "itemStyle": {
                    "borderRadius": 10,
                    "borderColor": '#fff',
                    "borderWidth": 2
                },
                "label": {
                    "show": False,
                    "position": 'center'
                },
                "emphasis": {
                    "label": {
                    "show": True,
                    "fontSize": 15,
                    "fontWeight": 'bold'
                    }
                },
                "labelLine": {
                    "show": False
                },
                "data": [
                    { "value": data["data"]["repository"]["open"]["totalCount"], "name": 'Open' },
                    { "value": data["data"]["repository"]["closed"]["totalCount"], "name": 'Closed' },
                ]
                }
            ]
            };
        self.data[self._get_hash(owner, repo)]['issue_count'] = option

        # Initialize the pull request data

    def pull_request_count(self, owner, repo ):
        query = """
            query ($owner: String!, $name: String!) {
            repository(owner: $owner, name: $name) {
                    open: pullRequests(states:OPEN) {
						totalCount
					}
					closed: pullRequests(states:CLOSED) {
						totalCount    
                    }
                }
            }        
        """

        variables = {
            "owner": owner,
            "name": repo,
        }

        data = self.req.post_query(query, variables)

        if data is None:
            return None

        
        option = {
            "tooltip": {
                "trigger": 'item'
            },
            "legend": {
                "top": '5%',
                "left": 'center'
            },
            "series": [
                {
                "name": 'Issue Count',
                "type": 'pie',
                "radius": ['40%', '70%'],
                "avoidLabelOverlap": False,
                "itemStyle": {
                    "borderRadius": 10,
                    "borderColor": '#fff',
                    "borderWidth": 2
                },
                "label": {
                    "show": False,
                    "position": 'center'
                },
                "emphasis": {
                    "label": {
                    "show": True,
                    "fontSize": 15,
                    "fontWeight": 'bold'
                    }
                },
                "labelLine": {
                    "show": False
                },
                "data": [
                    { "value": data["data"]["repository"]["open"]["totalCount"], "name": 'Open' },
                    { "value": data["data"]["repository"]["closed"]["totalCount"], "name": 'Closed' },
                ]
                }
            ]
            };
        self.data[self._get_hash(owner, repo)]['pull_request_count'] = option

        # Initialize the pull request data


    def pull_request_activity(self, owner, repo):
        data = self.req.post_rest(f"/repos/{owner}/{repo}/pulls",
                                  {"state": "all", "per_page": 100, "sort": "updated", "direction": "desc"})

        # data.extend(self.req.post_rest(f"/repos/{owner}/{repo}/pulls",
        #         {"state": "all", "per_page": 100, "page": 2, "sort": "created", "direction": "asc"}))

        if data is None:
            return None

        # Initialize lists to store the data for the x and y axis
        # x_data = []
        y_data_state = {}

        # Iterate through the pull requests
        for pull_request in data:
            # Extract the date when the pull request was created
            # created_at = datetime.strptime(pull_request["created_at"], "%Y-%m-%dT%H:%M:%SZ").date()

            # Extract the date when the pull request was updated
            updated_at = datetime.strptime(
                pull_request["updated_at"], "%Y-%m-%dT%H:%M:%SZ").date()

            # Append the date to the x data list
            # x_data.append(updated_at)
            updated_date_exist = y_data_state.get(updated_at, None)
            if updated_date_exist is None:
                y_data_state[updated_at] = {"open": 0, "closed": 0}

            # Check if the pull request is open or closed
            if pull_request["state"] == "open":
                # Increment the count for open pull requests
                y_data_state[updated_at]["open"] += 1
            else:
                # Increment the count for closed pull requests
                y_data_state[updated_at]["closed"] += 1

        # print(y_data_state)
        # zipped = zip(y_data_state.keys(), y_data_state.values())
        # zipped = sorted(zipped, key=lambda x: x[0])
        zipped = {k: v for k, v in sorted(y_data_state.items(), key=lambda item: item[0], reverse=False)}

        # Define the option for the stacked bar chart
        option = {
            "xAxis": {
                "data": list(zipped.keys())
            },
            "yAxis": {},
            "series": [
                {
                    "data": [v['open'] for _, v in zipped.items()],
                    "type": "bar",
                    "stack": "pull_requests",
                    "name":"open"
                },
                {
                    "data": [v['closed'] for _, v in zipped.items()],
                    "type": "bar",
                    "stack": "pull_requests",
                    "name":"closed"
                }
            ],
            "tooltip": {
                "trigger": 'axis',
            }
        }
        self.data[self._get_hash(owner, repo)
                  ]['pull_request_activity'] = option

    def pull_request_activity_ql(self, owner, repo):
        # Returns the number of pull requests opened and closed in the repository over the 12 months prior to the current date.
        now = datetime.now()
        one_year_ago = (now - timedelta(days=30)).date()

        query = """
            query ($owner: String!, $name: String!, $cursor: String) {
            repository(owner: $owner, name: $name) {
                pullRequests(first: 100, after: $cursor, states: [OPEN,CLOSED], orderBy: {field: UPDATED_AT, direction: DESC}) {
                nodes {
                    state
                    updatedAt
                }
                pageInfo {
                    endCursor
                    hasNextPage
                    }
                }
                }
            }        
        """

        variables = {
            "owner": owner,
            "name": repo,
            "cursor": None,
            # "query_date": one_year_ago.isoformat()
        }

        # Initialize the pull request data
        pull_requests = []
        while True:
            data = self.req.post_query(query, variables)
            # data = json.loads(res.text)
            latest_dt = datetime.strptime(
                data["data"]["repository"]["pullRequests"]["nodes"][-1]["updatedAt"], "%Y-%m-%dT%H:%M:%SZ").date()
            pull_requests.extend(
                data["data"]["repository"]["pullRequests"]["nodes"])
            if not data["data"]["repository"]["pullRequests"]["pageInfo"]["hasNextPage"]:
                break
            if latest_dt < one_year_ago:
                break
            variables["cursor"] = data["data"]["repository"]["pullRequests"]["pageInfo"]["endCursor"]

        combined = {}
        for pull_request in pull_requests:
            date = datetime.strptime(
                pull_request["updatedAt"], "%Y-%m-%dT%H:%M:%SZ").date()
            state = pull_request["state"]
            is_combined = combined.get(date, None)
            if is_combined is None:
                combined[date] = {"OPEN": 0, "CLOSED": 0}
            combined[date][state] += 1

        x_axis = list(sorted(combined.keys()))
        y_axis = {'open': [], 'closed': []}

        for date in x_axis:
            y_axis['open'].append(combined[date]['OPEN'])
            y_axis['closed'].append(combined[date]['CLOSED'])

        option = {
            "xAxis": {
                "type": 'category',
                "data": x_axis
            },
            "yAxis": {
                "type": 'value'
            },
            "series": [
                {
                    "data": y_axis['open'],
                    "type": 'bar',
                    "stack": 'pull_request',
                    "name": 'Open'
                },
                {
                    "data": y_axis['closed'],
                    "type": 'bar',
                    "stack": 'pull_request',
                    "name": 'Closed'
                }
            ],
            "tooltip": {
                "trigger": 'axis',
            }
        }
        # return option
        self.data[self._get_hash(owner, repo)
                  ]['pull_request_activity'] = option

    def star_activity(self, owner, repo):
        query = """
            query ($owner: String!, $name: String!, $cursor: String) {
                repository(owner: $owner, name: $name) {
                    stargazers(first: 100, after: $cursor, orderBy: {field: STARRED_AT, direction: DESC}) {
                    pageInfo {
                        endCursor
                        hasNextPage
                    }
                    edges {
                        starredAt
                    }
                }
            }
            }
        """
        variables = {
            "owner": owner,
            "name": repo,
            "cursor": None
        }

        # Fetch all pages
        results = {}
        max_fetch_count = 3
        current_fetch = 0
        while current_fetch <= max_fetch_count:
            data = self.req.post_query(
                query, variables)

            print(current_fetch)
            current_fetch += 1

            if data is None:
                return None
                
            # Extract the results
            for edge in data["data"]["repository"]["stargazers"]["edges"]:
                date_str = datetime.strptime(
                    edge["starredAt"], "%Y-%m-%dT%H:%M:%SZ").date()
                is_date_exist = results.get(date_str, None)
                print(date_str)

                if is_date_exist is None:
                    results[date_str] = 0
                results[date_str] += 1
            
            # Check if there are more pages
            if data["data"]["repository"]["stargazers"]["pageInfo"]["hasNextPage"]:
                variables["cursor"] = data["data"]["repository"]["stargazers"]["pageInfo"]["endCursor"]
            else:
                break

        # zipped = zip(results.keys(), results.values())
        # zipped = sorted(zipped, key=lambda x: x[0])
        zipped = {k: v for k, v in sorted(results.items(), key=lambda item: item[0], reverse=False)}

        # print([k for k, _ in zipped])
        # print([v for _, v in zipped])

        option = {
            "xAxis": {
                "type": "category",
                "data": list(zipped.keys())
            },
            "yAxis": {
                "type": "value"
            },
            "series": [
                {
                    "data": list(zipped.values()),
                    "type": "line",
                    "smooth": True, 
                    "showSymbol": False
                }
            ],
            "tooltip": {
                "trigger": 'axis',
            },
        }
        self.data[self._get_hash(owner, repo)
                  ]['star_activity'] = option

    def get_top_contributors(self, owner, repo):
        data = self.req.post_rest(f"/repos/{owner}/{repo}/pulls",
                                  {"per_page": 100})

        # Initialize variables to track contributors and their commit count
        contributors = {}

        # Fetch all contributors from API
        # page = 1
        variables = {
            "per_page": 100
        }
        # Send GET request to API endpoint
        data = self.req.post_rest(f"/repos/{owner}/{repo}/contributors", variables=variables, fetch_all=False)
        if data is None:
            return None
        
        # Add contributors and their commit count to dictionary
        for user in data:
            contributor_exist = contributors.get(user['login'], None)
            if contributor_exist is None:
                contributors[user['login']] = {
                    "avatar_url": user['avatar_url'],
                    "html_url": user['html_url'],
                    "contributions": user['contributions']
                }
            else:
                contributors[user['login']]["contributions"] += user['contributions']

        print(contributors)
        # Sort contributors by commit count in descending order
        contributors = {k: v for k, v in sorted(contributors.items(), key=lambda item: item[1]["contributions"], reverse=False)}

        # Get top 10 contributors
        top_10_contributors = dict(list(contributors.items())[:10])


        self.data[self._get_hash(owner, repo)]['top_contributors'] = contributors


from firestore import FirestoreDB
from update import Update
from request_actor import GRequest
import os
import pytest
from dotenv import load_dotenv
from datetime import datetime
load_dotenv()


"""
Methods:
- seed(): seeds the database with data for all repositories in the ecosystem
- init_overall(): initializes the overall_data dictionary with default values for the overall statistics
- write_overall(): generates and writes the overall statistics to the database
- fetch_and_write(): fetches and writes data for a single repository to the database
- overall_total_project_count(): generates and writes the total number of projects in the ecosystem to the database
- overall_top_contributors(): generates and writes the top contributors for the ecosystem to the database
- overall_recent_commits(): generates and writes the recent commits for the ecosystem to the database
- overall_pull_request_count(): generates and writes the pull request count for the ecosystem to the database
- overall_issue_count(): generates and writes the issue count for the ecosystem to the database
- overall_issue_activity(): generates and writes the issue activity for the ecosystem to the database
- overall_code_frequency(): generates and writes the code frequency for the ecosystem to the database
- overall_commit_history(): generates and writes the commit history for the ecosystem to the database

Fields:
- make_request: an instance of the GRequest class for making requests to the GitHub API
- data: a dictionary for storing data fetched from the GitHub API
- collection_index: an integer for keeping track of the current collection index
- fire_app: an instance of the FirestoreDB class for accessing the Firebase app
- db: an instance of the FirestoreDB class for accessing the Firestore database
- info_collection_ref: a reference to the collection for storing repository info documents
- data_collection_ref: a reference to the collection for storing repository data documents
- overall_collection_ref: a reference to the collection for storing overall statistics documents
- all_repo_names: a list of dictionaries containing the names of all repositories in the ecosystem
"""

# USED FOR TESTING
ECOSYSTEM = "polka"
OWNER = "paritytech"
REPO = "polkadot"


@pytest.fixture
def test_instance():
    update_ctx = Update("polkadot")
    update_ctx.init_overall()
    return update_ctx

class TestUpdate:
    # Tests that the database is seeded correctly with valid data. 
    def test_commit_history(self, test_instance):
        option = test_instance.commit_history(OWNER, REPO)

        # Check that the function returns a valid option
        assert option is not None

        # Check that the option has the expected keys
        assert set(option.keys()) == {"xAxis", "yAxis", "series"}

        # Check that the xAxis is a dictionary with the expected keys
        assert set(option["xAxis"].keys()) == {"data"}

        # Check that the yAxis is a dictionary
        assert isinstance(option["yAxis"], dict)

        # Check that the series is a list with one element
        assert isinstance(option["series"], list)
        assert len(option["series"]) == 1

        # Check that the series element is a dictionary with the expected keys
        series_element = option["series"][0]
        assert set(series_element.keys()) == {"data", "type"}

        # Check that the data for the series element is a list with the expected length
        data = series_element["data"]
        assert isinstance(data, list)
        assert len(data) == 52


def test_code_frequency(test_instance):
    # Call the function
    result = test_instance.code_frequency(OWNER, REPO)

    # Check that the function returns a dictionary
    assert isinstance(result, dict)

    # Check that the dictionary has the expected keys
    expected_keys = ["xAxis", "yAxis", "series"]
    assert all(key in result.keys() for key in expected_keys)

    # Check that the "xAxis" key has a non-empty list as its value
    assert isinstance(result["xAxis"], dict)
    assert "data" in result["xAxis"].keys()
    assert isinstance(result["xAxis"]["data"], list)
    assert len(result["xAxis"]["data"]) > 0

    # Check that the "series" key has a list with two dictionaries as its value
    assert isinstance(result["series"], list)
    assert len(result["series"]) == 2
    assert isinstance(result["series"][0], dict)
    assert isinstance(result["series"][1], dict)



def test_issue_activity(test_instance):
    # Call the function
    recent_issues, result = test_instance.issue_activity(OWNER, REPO)

    # Check that the function returns a tuple with two items
    assert isinstance(result, dict)
    assert isinstance(recent_issues, list)

    # Check that the dictionary has the expected keys
    expected_keys = ["xAxis", "yAxis", "series"]
    assert all(key in result.keys() for key in expected_keys)

    # Check that the "xAxis" key has a non-empty list as its value
    assert isinstance(result["xAxis"], dict)
    assert "data" in result["xAxis"].keys()
    assert isinstance(result["xAxis"]["data"], list)
    assert len(result["xAxis"]["data"]) > 0

    # Check that the "series" key has a list with two dictionaries as its value
    assert isinstance(result["series"], list)
    assert len(result["series"]) == 2
    assert isinstance(result["series"][0], dict)
    assert isinstance(result["series"][1], dict)

    # Check that the recent_issues list has at most 5 issues
    assert len(recent_issues) <= 5


def test_issue_count(test_instance):
    # Call the function
    result = test_instance.issue_count(OWNER, REPO)

    # Check that the function returns a dictionary
    assert isinstance(result, dict)

    # Check that the dictionary has the expected keys
    expected_keys = ["series"]
    assert all(key in result.keys() for key in expected_keys)

    # Check that the "series" key has a list with one dictionary as its value
    assert isinstance(result["series"], list)
    assert len(result["series"]) == 1
    assert isinstance(result["series"][0], dict)

    # Check that the dictionary has been updated with the correct data
    expected_open_count = test_instance.overall_data["issue_count"]["series"][0]["data"][0]["value"]  # expected open issue count
    expected_closed_count = test_instance.overall_data["issue_count"]["series"][0]["data"][1]["value"]  # expected closed issue count
    assert result["series"][0]["data"][0]["value"] == expected_open_count
    assert result["series"][0]["data"][1]["value"] == expected_closed_count


def test_pull_request_count(test_instance):
    # Call the function
    result = test_instance.pull_request_count(OWNER, REPO)

    # Check that the function returns a dictionary
    assert isinstance(result, dict)

    # Check that the dictionary has the expected keys
    expected_keys = ["series"]
    assert all(key in result.keys() for key in expected_keys)

    # Check that the "series" key has a list with one dictionary as its value
    assert isinstance(result["series"], list)
    assert len(result["series"]) == 1
    assert isinstance(result["series"][0], dict)

    # Check that the dictionary has been updated with the correct data
    expected_open_count = test_instance.overall_data["pull_request_count"]["series"][0]["data"][0]["value"]  # expected open PR count
    expected_closed_count = test_instance.overall_data["pull_request_count"]["series"][0]["data"][1]["value"]  # expected closed PR count
    assert result["series"][0]["data"][0]["value"] == expected_open_count
    assert result["series"][0]["data"][1]["value"] == expected_closed_count


def test_pull_request_activity(test_instance):
    # Call the function
    result = test_instance.pull_request_activity(OWNER, REPO)

    # Check that the function returns a dictionary
    assert isinstance(result, dict)

    # Check that the dictionary has the expected keys
    expected_keys = ["xAxis", "yAxis", "series"]
    assert all(key in result.keys() for key in expected_keys)

    # Check that the "series" key has a list with two dictionaries as its value
    assert isinstance(result["series"], list)
    assert len(result["series"]) == 2
    assert isinstance(result["series"][0], dict)
    assert isinstance(result["series"][1], dict)

    # Check that the dictionary has the expected values for the "xAxis" and "yAxis" keys
    assert result["xAxis"]["data"] is not None
    assert result["yAxis"] == {}

    # Check that the dictionary has the expected values for the "series" key
    expected_names = ["open", "closed"]
    for i, name in enumerate(expected_names):
        assert result["series"][i]["name"] == name
        assert result["series"][i]["type"] == "bar"
        assert result["series"][i]["stack"] == "pull_requests"
        assert isinstance(result["series"][i]["data"], list)

def test_star_activity(test_instance):
    result = test_instance.star_activity(OWNER, REPO)
    assert result is not None
    assert isinstance(result, dict)
    assert "xAxis" in result
    assert "yAxis" in result
    assert "series" in result
    assert "data" in result["series"][0]
    assert isinstance(result["series"][0]["data"], list)
    assert all(isinstance(date_str, str) for date_str in result["xAxis"]["data"])
    assert all(isinstance(count, int) for count in result["series"][0]["data"])
    assert all(datetime.strptime(date_str, "%Y-%m-%d").date() for date_str in result["xAxis"]["data"])

def test_top_contributors(test_instance):
    result = test_instance.top_contributors(OWNER, REPO)
    assert result is not None
    assert isinstance(result, list)
    assert len(result) == 4
    for contributor in result:
        assert isinstance(contributor, dict)
        assert "login" in contributor
        assert "avatar_url" in contributor
        assert "html_url" in contributor
        assert "contributions" in contributor

def test_recent_commits(test_instance):
    result = test_instance.recent_commits(OWNER, REPO)
    assert result is not None
    assert isinstance(result, list)
    assert len(result) == 5
    for commit in result:
        assert isinstance(commit, dict)
        assert "commit" in commit
        assert "author" in commit["commit"]
        assert "date" in commit["commit"]["author"]
        assert isinstance(commit["commit"]["author"]["date"], str)

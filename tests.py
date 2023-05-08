
from firestore import FirestoreDB
from update import Update
from request_actor import GRequest
import os
import pytest
from dotenv import load_dotenv
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

class TestUpdate:
    # Tests that the database is seeded correctly with valid data. 
    def test_commit_history(self):
        update_ctx = Update("polkadot")
        update_ctx.init_overall()
        option = update_ctx.commit_history(OWNER, REPO)

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

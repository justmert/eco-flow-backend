
from firestore import FirestoreDB
from update import Update
from request_actor import GRequest
import os


import pytest

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

class TestUpdate:
    # Tests that the database is seeded correctly with valid data. 
    def test_seed(self):
        # setup
        fire_ctx = FirestoreDB(admin_sdk_path='path/to/credentials.json', project_id='test-project')
        ecosystem = 'test-ecosystem'
        update = Update(fire_ctx, ecosystem)

        # execute
        update.seed()

        # assert
        assert update.overall_data['total_project_count'] == len(update.all_repo_names)
        assert update.overall_data['total_star_count'] >= 0
        assert update.overall_data['top_contributors'] != {}
        assert update.overall_data['commit_history']['xAxis']['data'] is not None
        assert update.overall_data['_code_frequency'] != {}
        assert update.overall_data['_issue_activity'] != {}
        assert update.overall_data['recent_issues'] != []
        assert update.overall_data['recent_commits'] != []
        assert update.overall_data['issue_count']['series'][0]['data'][0]['value'] >= 0
        assert update.overall_data['issue_count']['series'][0]['data'][1]['value'] >= 0
        assert update.overall_data['pull_request_count']['series'][0]['data'][0]['value'] >= 0
        assert update.overall_data['pull_request_count']['series'][0]['data'][1]['value'] >= 0

    # Tests that data is fetched and written correctly for a repository with valid input. 
    def test_fetch_and_write_valid(self, mocker):
        # setup
        fire_ctx = FirestoreDB(admin_sdk_path='path/to/credentials.json', project_id='test-project')
        ecosystem = 'test-ecosystem'
        update = Update(fire_ctx, ecosystem)
        repo = {'owner': 'test-owner', 'repo': 'test-repo'}
        mocker.patch.object(GRequest, 'github_post_rest_request', return_value={'data': {'repository': {'name': 'test-repo'}}})
        mocker.patch.object(GRequest, 'github_post_graphql_request', return_value={'data': {'repository': {'name': 'test-repo'}}})

        # execute
        update.fetch_and_write(repo)

        # assert
        assert update.data_collection_ref.document(f"{repo['owner']}-{repo['repo']}").get().exists

    # Tests that an error is raised when trying to fetch and write data for a non-existent repository. 
    def test_fetch_and_write_nonexistent(self, mocker):
        # setup
        fire_ctx = FirestoreDB(admin_sdk_path='path/to/credentials.json', project_id='test-project')
        ecosystem = 'test-ecosystem'
        update = Update(fire_ctx, ecosystem)
        repo = {'owner': 'nonexistent-owner', 'repo': 'nonexistent-repo'}
        mocker.patch.object(GRequest, 'github_post_rest_request', return_value=None)
        mocker.patch.object(GRequest, 'github_post_graphql_request', return_value=None)

        # execute and assert
        with pytest.raises(Exception):
            update.fetch_and_write(repo)

    # Tests that an error is raised when trying to fetch and write data for a repository with invalid input. 
    def test_fetch_and_write_invalid(self, mocker):
        # setup
        fire_ctx = FirestoreDB(admin_sdk_path='path/to/credentials.json', project_id='test-project')
        ecosystem = 'test-ecosystem'
        update = Update(fire_ctx, ecosystem)
        repo = {'owner': '', 'repo': ''}
        mocker.patch.object(GRequest, 'github_post_rest_request', return_value=None)
        mocker.patch.object(GRequest, 'github_post_graphql_request', return_value=None)

        # execute and assert
        with pytest.raises(Exception):
            update.fetch_and_write(repo)

    # Tests that overall data is written correctly to the database. 
    def test_write_overall(self, mocker):
        # setup
        fire_ctx = FirestoreDB(admin_sdk_path='path/to/credentials.json', project_id='test-project')
        ecosystem = 'test-ecosystem'
        update = Update(fire_ctx, ecosystem)
        mocker.patch.object(update, 'overall_commit_history')
        mocker.patch.object(update, 'overall_code_frequency')
        mocker.patch.object(update, 'overall_issue_activity')
        mocker.patch.object(update, 'overall_issue_count')
        mocker.patch.object(update, 'overall_pull_request_count')
        mocker.patch.object(update, 'overall_recent_commits')
        mocker.patch.object(update, 'overall_top_contributors')
        mocker.patch.object(update, 'overall_total_project_count')
        mocker.patch.object(update, 'overall_star_count')

        # execute
        update.write_overall()

        # assert
        assert update.overall_commit_history.called
        assert update.overall_code_frequency.called
        assert update.overall_issue_activity.called
        assert update.overall_issue_count.called
        assert update.overall_pull_request_count.called
        assert update.overall_recent_commits.called
        assert update.overall_top_contributors.called
        assert update.overall_total_project_count.called
        assert update.overall_star_count.called

    # Tests that data is retrieved correctly from the database. 
    def test_get_data(self):
        # setup
        fire_ctx = FirestoreDB(admin_sdk_path='path/to/credentials.json', project_id='test-project')
        ecosystem = 'test-ecosystem'
        update = Update(fire_ctx, ecosystem)

        # execute
        data = update.get_data

        # assert
        assert data is not None

    def test_code_frequency():
        owner = "paritytech"
        repo = "polkadot"

        fire_ctx = FirestoreDB(admin_sdk_path='path/to/credentials.json', project_id='test-project')
        ecosystem = 'test-ecosystem'
        update = Update(fire_ctx, ecosystem)


        option = update.code_frequency(owner, repo)

        # Check that the function returns a valid option
        assert option is not None

        # Check that the option has the expected keys
        assert set(option.keys()) == {"xAxis", "yAxis", "series"}

        # Check that the xAxis is a dictionary with the expected keys
        assert set(option["xAxis"].keys()) == {"data"}

        # Check that the yAxis is a dictionary
        assert isinstance(option["yAxis"], dict)

        # Check that the series is a list with two elements
        assert isinstance(option["series"], list)
        assert len(option["series"]) == 2

        # Check that the series elements are dictionaries with the expected keys
        for series_element in option["series"]:
            assert set(series_element.keys()) == {"data", "type", "stack"}

            # Check that the data for the series element is a list with the expected length
            data = series_element["data"]
            assert isinstance(data, list)
            assert len(data) == 52

        # Check that the overall_data has been updated correctly
        assert update.overall_data["_code_frequency"] != {}


    def test_commit_history():
        owner = "paritytech"
        repo = "polkadot"
        
        fire_ctx = FirestoreDB(admin_sdk_path='path/to/credentials.json', project_id='test-project')
        ecosystem = 'test-ecosystem'
        update = Update(fire_ctx, ecosystem)

        option = update.commit_history(owner, repo)

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

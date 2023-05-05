    # Tests that the database is seeded correctly with valid data. 
    def test_seed(self):
        # Happy path test
        # Ensure that the database is seeded correctly with valid data
        fire_ctx = FirestoreDB(admin_sdk_path='path/to/credentials.json', project_id='test-project')
        update = Update(fire_ctx, 'test-ecosystem')
        update.seed()
        overall_data = update.overall_data
        assert overall_data['total_project_count'] == 3
        assert overall_data['total_star_count'] == 10
        assert len(overall_data['top_contributors']) == 4
        assert len(overall_data['recent_commits']) == 5
        assert overall_data['issue_count']['series'][0]['data'][0]['value'] == 2
        assert overall_data['issue_count']['series'][0]['data'][1]['value'] == 1
        assert overall_data['pull_request_count']['series'][0]['data'][0]['value'] == 1
        assert overall_data['pull_request_count']['series'][0]['data'][1]['value'] == 1



    # Tests that data is fetched and written correctly for a repository with valid inputs.  
    def test_fetch_and_write_valid(self):
        # Happy path test
        # Ensure that data is fetched and written correctly for a repository with valid inputs
        fire_ctx = FirestoreDB(admin_sdk_path='path/to/credentials.json', project_id='test-project')
        update = Update(fire_ctx, 'test-ecosystem')
        repo = {'owner': 'test-owner', 'repo': 'test-repo'}
        update.fetch_and_write(repo)
        data_doc_ref = update.data_collection_ref.document(f"{repo['owner']}-{repo['repo']}")
        data = data_doc_ref.get().to_dict()

        # Assert that all keys are present in the fetched data
        expected_keys = ['commit_history', 'code_frequency', 'recent_issues', 'issue_activity',
                         'issue_count', 'pull_request_count', 'pull_request_activity',
                         'star_activity', 'top_contributors', 'recent_commits']
        assert set(data.keys()) == set(expected_keys)

        # Assert that all values are not None
        for key in expected_keys:
            assert data[key] is not None, f"{key} should not be None"


    # Tests that API errors are handled correctly during data fetching. 
    def test_api_error_handling(self, monkeypatch):
        # Edge case test
        # Ensure that API errors are handled correctly during data fetching
        def mock_post_graphql_request(_query, variables=None):
            return None

        monkeypatch.setattr(GRequest, 'github_post_graphql_request', mock_post_graphql_request)

        fire_ctx = FirestoreDB(admin_sdk_path='path/to/credentials.json', project_id='test-project')
        update = Update(fire_ctx, 'test-ecosystem')
        repo = {'owner': 'test-owner', 'repo': 'test-repo'}
        update.fetch_and_write(repo)
        data_doc_ref = update.data_collection_ref.document(f"{repo['owner']}-{repo['repo']}")
        data = data_doc_ref.get().to_dict()
        assert data is None



    # Tests that unexpected responses from the API are handled correctly. 
    def test_unexpected_response_handling(self, monkeypatch):
        # Edge case test
        # Ensure that unexpected responses from the API are handled correctly
        def mock_post_graphql_request(_query, variables=None):
            return {'data': {'repository': {'name': 'test-repo', 'owner': {'login': 'test-owner'}}}}

        monkeypatch.setattr(GRequest, 'github_post_graphql_request', mock_post_graphql_request)

        fire_ctx = FirestoreDB(admin_sdk_path='path/to/credentials.json', project_id='test-project')
        update = Update(fire_ctx, 'test-ecosystem')
        repo = {'owner': 'test-owner', 'repo': 'test-repo'}
        update.fetch_and_write(repo)
        data_doc_ref = update.data_collection_ref.document(f"{repo['owner']}-{repo['repo']}")
        data = data_doc_ref.get().to_dict()
        assert data is None


    # Tests that unexpected errors during database operations are handled correctly. 
    def test_unexpected_error_handling(self, monkeypatch):
        # Edge case test
        # Ensure that unexpected errors during database operations are handled correctly
        def mock_commit_history(owner, repo):
            raise Exception('Unexpected error')

        monkeypatch.setattr(Update, 'commit_history', mock_commit_history)

        fire_ctx = FirestoreDB(admin_sdk_path='path/to/credentials.json', project_id='test-project')
        update = Update(fire_ctx, 'test-ecosystem')
        repo = {'owner': 'test-owner', 'repo': 'test-repo'}
        update.fetch_and_write(repo)
        data_doc_ref = update.data_collection_ref.document(f"{repo['owner']}-{repo['repo']}")
        data = data_doc_ref.get().to_dict()
        assert data is None



    # Tests that data fetching and writing fails gracefully for a repository with invalid inputs.  
    def test_fetch_and_write_invalid(self):
        # Edge case test
        # Ensure that data fetching and writing fails gracefully for a repository with invalid inputs
        fire_ctx = FirestoreDB(admin_sdk_path='path/to/credentials.json', project_id='test-project')
        update = Update(fire_ctx, 'test-ecosystem')
        repo = {'owner': 'invalid-owner', 'repo': 'invalid-repo'}
        
        # Wrap the fetch_and_write call in a try-except block to handle exceptions
        try:
            update.fetch_and_write(repo)
        except Exception as e:
            # Assert that the exception message is as expected
            assert str(e) == f"Failed to fetch and write data for repository {repo['owner']}/{repo['repo']}"

        # Check if the data was not written to the database
        data_doc_ref = update.data_collection_ref.document(f"{repo['owner']}-{repo['repo']}")
        data_doc = data_doc_ref.get()
        
        # Assert that the document does not exist in the database
        assert not data_doc.exists


        # Tests that overall data is written correctly to the database.  
    def test_write_overall(self, mocker):
        # Happy path test
        mocker.patch.object(Update, 'overall_commit_history')
        mocker.patch.object(Update, 'overall_code_frequency')
        mocker.patch.object(Update, 'overall_issue_activity')
        mocker.patch.object(Update, 'overall_issue_count')
        mocker.patch.object(Update, 'overall_pull_request_count')
        mocker.patch.object(Update, 'overall_recent_commits')
        mocker.patch.object(Update, 'overall_top_contributors')
        mocker.patch.object(Update, 'overall_total_project_count')
        mocker.patch.object(Update, 'overall_star_count')

        update = Update(None, "test_ecosystem")
        update.overall_data = {
            "commit_history": {
                "xAxis": {"data": None},
                "yAxis": {},
                "series": [
                    {"data": [], "type": "line"}
                ],
            },
            "_code_frequency": {},
            "_issue_activity": {},
            "recent_issues": [],
            "recent_commits": [],
            "issue_count": {
                "series": [
                    {
                        "data": [
                            {"value": 0, "name": 'Open'},
                            {"value": 0, "name": 'Closed'},
                        ]
                    }
                ]
            },
            "pull_request_count": {
                "series": [
                    {
                        "data": [
                            {"value": 0, "name": 'Open'},
                            {"value": 0, "name": 'Closed'},
                        ]
                    }
                ]
            },
            "top_contributors": {},
            "total_project_count": 0,
            "total_star_count": 0
        }

        update.write_overall()

        update.overall_commit_history.assert_called_once()
        update.overall_code_frequency.assert_called_once()
        update.overall_issue_activity.assert_called_once()
        update.overall_issue_count.assert_called_once()
        update.overall_pull_request_count.assert_called_once()
        update.overall_recent_commits.assert_called_once()
        update.overall_top_contributors.assert_called_once()
        update.overall_total_project_count.assert_called_once()
        update.overall_star_count.assert_called_once()



            # Tests that top contributors are handled correctly when there are no contributors.  
    def test_top_contributors_empty(self, mocker):
        # Edge case test
        mocker.patch.object(Update, 'top_contributors', return_value={})

        update = Update(None, "test_ecosystem")
        update.overall_data = {
            "top_contributors": {}
        }

        update.overall_top_contributors()

        update.overall_collection_ref.document.assert_called_with(u'_overall')
        update.overall_collection_ref.document().set.assert_called_with({
            u'top_contributors': None,
        }, merge=True)


            # Tests that data is retrieved correctly from the database.  
    def test_get_data(self, mocker):
        # General behavior test
        mocker.patch.object(FirestoreDB, 'get_db')
        mocker.patch.object(FirestoreDB, 'get_app')
        mocker.patch.object(FirestoreDB, 'collection')
        mocker.patch.object(FirestoreDB, 'document')
        mocker.patch.object(GRequest, 'github_post_rest_request', return_value=[{"name": "test_repo"}])

        update = Update(FirestoreDB(None, "test_project"), "test_ecosystem")
        update.all_repo_names = [{"owner": "test_owner", "repo": "test_repo"}]

        data = update.get_data

        assert data == [{"name": "test_repo"}]
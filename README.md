# Set-up

Create .env file in the root directory and add the following variables:

```
GITHUB_BEARER_KEY # GitHub API key
ADMIN_SDKS_PATH # Path to the admin SDKs
```

## Install dependencies

```
pip3 install -r requirements.txt

```

## Test the app

In the root directory, run the following command:

```
pytest tests.py
```


## Run the app

In the root directory, run the following command:

```
python3 .
```

This command will execute the script that fetches the data from the GitHub API and saves it in the Firebase Firestore database.


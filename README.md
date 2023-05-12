# Set-up

Create .env file in the root directory and add the following variables:

```
GITHUB_BEARER_KEY # GitHub API key
ADMIN_SDK_PATH # Path to the admin SDK file
PROJECT_LIST # Path to the project list file
```

> Know that admin sdk file and project list files needs to be in this format:
> `<ecosystenm_name>-admin-sdk.json` and `<ecosystenm_name>.txt` respectively.
> Also <ecosystem_name.txt> needs to include line by line project names. For example: `paritytech/substrate`

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

Scripts run in the following order:

```
python3 seed.py --ecosystem <ecosystem_name>  # to feed the database with projects

python3 .  # to update project info in the database
```


# Flow App Backend

If you didn't read the [frontend documentation](https://github.com/justmert/eco-flow-frontend/blob/master/README.md), please do so before continuing. Through the documentation, we will use the arbitrary variable `<ecosystem_name>` to refer to the blockchain ecosystem you are working on. For example, if you are working on Polkadot, you can use 'polka' as the ecosystem name. Just know that, this variable needs to be consistent throughout the documentation (also in the backend documentation).

## Configuration

1. Create a text file named `<ecosystem_name>.txt` that includes the list of projects you want to add to the firebase database. For example, if you are working on Polkadot, you can create a file named `polka.txt` and add the following projects to the file:

> <ecosystem_name.txt> needs to include line by line project names. For example,
>
> ```
> paritytech/ink
> polkadot-js/apps
> polkadot-js/extension
> ```

2. Download Google Cloud Firebase Admin SDK from Firebase project settings, and rename to `<ecosystem_name>-admin-sdk.json`. Go to '<https://console.firebase.google.com/project/[FIREBASE_PROJECT_NAME]/settings/serviceaccounts/adminsdk>', and click 'Generate new private key' button.

3. Create a file named `.env` in the root directory and add the following variables to the file:

```
ECOSYSTEM_NAME # <ecosystem_name> that you use through the documentation. For example, 'polka'.
FIREBASE_PROJECT_ID # Firebase project ID.
GITHUB_BEARER_KEY # GitHub API key.
ADMIN_SDK_PATH # Path to the Google Cloud Admin SDK file that you have downloaded before.
PROJECT_LIST # Path to the project list file that you have created before.
```

## Install dependencies

```
pip3 install -r requirements.txt
```

The backend consists of two scripts: `seed.py` and `main.py`. `seed.py` is used to feed the database with projects and `main.py` is used to update the project info in the database. For example, if you want to integrate a new project to the database, you need to run `seed.py` first and then `main.py`. If you want to update the project info in the database, you only need to run `main.py`.

## Seed the database

Seeding the database is a one-time process. You only need to run this script when you want to integrate a new project to the database. In the root directory, run the following command:

```
python3 seed.py --ecosystem <ecosystem_name>
```

This script reads from the `<ecosystem_name>.txt` file and adds the these projects to the database.

> <ecosystem_name> indicates the ecosystem you want to update for example 'polka'.

## Update the database

In the root directory, run the following command:

```
python3 .
```

This script updates the database with the latest project info. Just make sure that you have set the .env variables correctly.

## Test the app

In the root directory, run the following command:

```
pytest tests.py
```

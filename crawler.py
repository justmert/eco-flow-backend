import firebase_admin
from firebase_admin import firestore, credentials
import os 
import argparse
from dotenv import load_dotenv
from projects import projects
import toml
import requests
 
load_dotenv()

parser = argparse.ArgumentParser(description='Name a ecosystem.')
parser.add_argument("--ecosystem", help='ecosystem name',type=str)
args = parser.parse_args()


found_project = [p for p in projects if p[0] == args.ecosystem][0]
t_project_short_id, t_project_id, t_project_name = found_project
print('crawling...')

# Download the file from the URL
url = f'https://raw.githubusercontent.com/electric-capital/crypto-ecosystems/master/data/ecosystems/f/{t_project_short_id}.toml'
response = requests.get(url)
content = response.content.decode('utf-8')

# Parse the TOML file
data = toml.loads(content)

# Extract owner and repo name for each repository
repos = data['repo']
repo_list = []
for repo in repos:
    url_parts = repo['url'].split('/')
    owner = url_parts[-2]
    repo_name = url_parts[-1]
    repo_list.append([owner, repo_name])

print(f"{len(repo_list)} repositories found")
print('Adding the following projects to the database:')


cred = credentials.Certificate(f"{os.environ['ADMIN_SDKS_PATH']}/{t_project_short_id}-admin-sdk.json")
app = firebase_admin.initialize_app(cred)
db = firestore.client()

project_array_ref = db.collection(f'{t_project_short_id}-repositories-data').document('_names')

# with open(f"initial_projects/{t_project_short_id}.txt") as file:
#     lines = [line.strip() for line in file]

# lines = [line for line in lines if line != '']

for owner, name in repo_list:
    project_array_ref.update({u'repository_names': firestore.ArrayUnion([{
        "owner": owner,
        "repo": name
    }])})
    print(f' - {owner}/{name} added to the database')

print('Done')


if __name__ == '__main__':
    pass

import firebase_admin
from firebase_admin import firestore, credentials
import os 
import argparse
from dotenv import load_dotenv
from projects import projects
load_dotenv()

parser = argparse.ArgumentParser(description='Name a ecosystem.')
parser.add_argument("--ecosystem", help='ecosystem name',type=str)
args = parser.parse_args()

print('Adding the following projects to the database:')

found_project = [p for p in projects if p[0] == args.ecosystem][0]
t_project_short_id, t_project_id, t_project_name = found_project

cred = credentials.Certificate(f"{os.environ['ADMIN_SDKS_PATH']}/{t_project_short_id}-admin-sdk.json")
app = firebase_admin.initialize_app(cred)
db = firestore.client()

project_array_ref = db.collection(f'{t_project_short_id}-repositories-data').document('_names')

with open(f"initial_projects/{t_project_short_id}.txt") as file:
    lines = [line.strip() for line in file]

lines = [line for line in lines if line != '']

for project_owner_name in lines:
    print(project_owner_name)
    owner, name = project_owner_name.split('/')
    project_array_ref.update({u'repository_names': firestore.ArrayUnion([{
        "owner": owner,
        "repo": name
    }])})
    print(f' - {owner}/{name} added to the database')

print('Done')


if __name__ == '__main__':
    pass

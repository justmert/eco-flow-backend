import firebase_admin
from firebase_admin import firestore, credentials
import os 
import argparse
from dotenv import load_dotenv
load_dotenv()

parser = argparse.ArgumentParser(description='Process a list of names.')
parser.add_argument('names', nargs='+', help='list of names')
args = parser.parse_args()

print('Adding the following projects to the database:')

cred = credentials.Certificate(os.getenv('FIREBASE_ADMIN_SDK_PATH'))
app = firebase_admin.initialize_app(cred)
db = firestore.client()

project_array_ref = db.collection(
    os.getenv('FIREBASE_DATA_COLLECTION')).document('_names')

for project_owner_name in args.names:
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

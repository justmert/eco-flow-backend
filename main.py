from dotenv import load_dotenv
import os
from update import Update 
from firestore import FirestoreDB
from projects import already_created_projects, projects
load_dotenv()

class Main():
    def __init__(self):
        for project_short_id, project_id, project_name in already_created_projects + projects:
            print()
            print('-'*50)
            print(f'Processing {project_name}')
            print('-'*50)
            self.admin_sdk_path = f"{os.environ['ADMIN_SDKS_PATH']}/{project_short_id}-admin-sdk.json"
            if not os.path.exists(self.admin_sdk_path):
                raise Exception(f'Admin SDK file not found: {self.admin_sdk_path}')
            print(f'Using {self.admin_sdk_path} to seed the database')

            self.fire_ctx = FirestoreDB(self.admin_sdk_path, project_id)
            self.fetch_ctx = Update(self.fire_ctx, project_short_id)
            self.update_db()

    def update_db(self):
        self.fetch_ctx.seed()




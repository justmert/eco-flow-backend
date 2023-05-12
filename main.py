from dotenv import load_dotenv
import os
from update import Update 
from firestore import FirestoreDB
from projects import projects
import schedule
import time
load_dotenv()

class Main():
    def __init__(self):
        for project_short_id, project_id, project_name in projects:
            print()
            print('-'*50)
            print(f'Processing {project_name}')
            print('-'*50)
            self.admin_sdk_path = f"{os.environ['ADMIN_SDK_PATH']}"
            if not os.path.exists(self.admin_sdk_path):
                raise Exception(f'Admin SDK file not found: {self.admin_sdk_path}')

            self.fire_ctx = FirestoreDB(self.admin_sdk_path, project_id)
            self.fetch_ctx = Update(project_short_id, fire_ctx=self.fire_ctx)
            print(f'Using {self.admin_sdk_path} to seed the database')
            self.update_db()
            
            print("Starting the scheduler")
            schedule.every().day.at("00:00").do(self.update_db)
            while 1:
                schedule.run_pending()
                time.sleep(1)


    def update_db(self):
        self.fetch_ctx.seed()




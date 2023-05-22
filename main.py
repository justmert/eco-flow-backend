from dotenv import load_dotenv
import os
from update import Update 
from firestore import FirestoreDB
import schedule
import time
load_dotenv()

class Main():
    def __init__(self):
        print()
        print('-'*50)
        self.admin_sdk_path = f"{os.environ['ADMIN_SDK_PATH']}"
        if not os.path.exists(self.admin_sdk_path):
            raise Exception(f'Admin SDK file not found: {self.admin_sdk_path}')

        self.fire_ctx = FirestoreDB(self.admin_sdk_path, os.environ['FIREBASE_PROJECT_ID'])
        self.fetch_ctx = Update(os.environ['ECOSYSTEM_NAME'], fire_ctx=self.fire_ctx)
        print(f'Using {self.admin_sdk_path} to seed the database')
        self.update_db()
        
        print("Starting the scheduler")
        schedule.every().day.at("00:00").do(self.update_db)
        while 1:
            schedule.run_pending()
            time.sleep(1)


    def update_db(self):
        self.fetch_ctx.seed()




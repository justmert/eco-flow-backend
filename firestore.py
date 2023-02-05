import firebase_admin
from firebase_admin import firestore, credentials
import os 

class FirestoreDB:
    def __init__(self):
        
        # os.environ["FIRESTORE_EMULATOR_HOST"] = "localhost:8080"
        # os.environ["GCLOUD_PROJECT"] = "lenspulse-20592"
        # os.environ["GOOGLE_CLOUD_PROJECT"] = "lenspulse-20592"

        # Use a service account.
        cred = credentials.Certificate('./firebase-adminsdk.json')
        self.app = firebase_admin.initialize_app(cred)
        self.db = firestore.client()

    @property
    def get_db(self):
        return self.db

    @property
    def get_app(self):
        return self.app

        


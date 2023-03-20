import firebase_admin
from firebase_admin import firestore, credentials
import os 

class FirestoreDB:
    def __init__(self, admin_sdk_path, project_id):
        # Use a service account.
        cred = credentials.Certificate(admin_sdk_path)
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = admin_sdk_path
        self.app = firebase_admin.initialize_app(cred, {
        'projectId': project_id
        }, project_id)
        self.db = firestore.Client()
        
    @property
    def get_db(self):
        return self.db

    @property
    def get_app(self):
        return self.app
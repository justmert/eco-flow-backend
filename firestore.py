import firebase_admin
from firebase_admin import firestore, credentials
import os 

class FirestoreDB:
    def __init__(self):
        # Use a service account.
        cred = credentials.Certificate(os.getenv('FIREBASE_ADMIN_SDK_PATH'))
        self.app = firebase_admin.initialize_app(cred)
        self.db = firestore.client()

    @property
    def get_db(self):
        return self.db

    @property
    def get_app(self):
        return self.app

        


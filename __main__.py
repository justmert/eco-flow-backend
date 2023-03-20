from main import Main
from dotenv import load_dotenv
load_dotenv()


if __name__ == '__main__':
    main_p = Main() # instantiate the Fetch class
    main_p.update_db() # call the update_db method

import pymysql

from dotenv import load_dotenv
import os
load_dotenv()


connection = pymysql.connect(
    
    host=os.environ["DB_host"],
    user=os.environ["DB_user"],
    password=os.environ["DB_password"],
    database=os.environ["DB_database"],
    port=int(os.environ["DB_port"])

    # host="localhost",
    # user="root",
    # password="Hafeez1@",
    # database="Library",
    # port=3306

)
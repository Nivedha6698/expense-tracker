from sqlalchemy import create_engine
from dotenv import load_dotenv
import os
from sqlalchemy import text

load_dotenv()

db_user = os.getenv('DB_USER')
db_pass = os.getenv('DB_PASSWORD')
db_host = os.getenv('DB_HOST')
db_name = os.getenv('DB_NAME')

# Connect WITHOUT DB
engine = create_engine(f"mysql+pymysql://{db_user}:{db_pass}@{db_host}")
print(db_host)

with engine.connect() as conn:
    conn.execute(text(f"CREATE DATABASE IF NOT EXISTS `{db_name}`"))
    print("✅ Database created successfully!")
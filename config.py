import os

DATABASE_HOST = os.environ["DATABASE_HOST"]
DATABASE_PORT = int(os.environ["DATABASE_PORT"])
DATABASE_USER = os.environ["DATABASE_USER"]
DATABASE_PASS = os.environ["DATABASE_PASS"]

class Configuration:
	SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{DATABASE_USER}:{DATABASE_PASS}@{DATABASE_HOST}:{DATABASE_PORT}/mdszadatak"
from flask import Flask

from config import Configuration
from endpoints.zaposleni import zaposleni_bp

from models.mdszadatak import database

application = Flask(__name__)
application.config.from_object(Configuration)

database.init_app(application)

application.register_blueprint(zaposleni_bp)

if __name__ == "__main__":
	application.run(host="0.0.0.0")
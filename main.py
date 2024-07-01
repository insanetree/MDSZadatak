from flask import Flask

from endpoints.zaposleni import zaposleni_bp

application = Flask(__name__)

application.register_blueprint(zaposleni_bp)

if __name__ == "__main__":
	application.run(host="0.0.0.0")
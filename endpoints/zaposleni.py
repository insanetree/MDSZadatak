from flask import Blueprint

zaposleni_bp = Blueprint("zaposleni", __name__, url_prefix="/zaposleni")

@zaposleni_bp.route("/avg_salary", methods=["GET"])
def avg_salary():
	pass

@zaposleni_bp.route("/third_highest_salary", methods=["GET"])
def third_highest_salary():
	pass
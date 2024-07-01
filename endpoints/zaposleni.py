from flask import Blueprint
from flask import jsonify

from sqlalchemy import func
from sqlalchemy import distinct
from sqlalchemy import desc

from models.mdszadatak import database
from models.mdszadatak import Employee

zaposleni_bp = Blueprint("zaposleni", __name__, url_prefix="/zaposleni")

@zaposleni_bp.route("/avg_salary", methods=["GET"])
def avg_salary():
	result = database.session.query(func.avg(Employee.salary)).one()
	return jsonify({"avg_salary": float(result[0])}), 200

@zaposleni_bp.route("/third_highest_salary", methods=["GET"])
def third_highest_salary():
	result = database.session.query(distinct(Employee.salary)).order_by(desc(Employee.salary)).limit(1).offset(2).one()
	return jsonify({"third_highest": int(result[0])}), 200

@zaposleni_bp.route("/like_a", methods=["GET"])
def like_a():
	result = Employee.query.filter(Employee.firstname.like("a%")).all()
	return jsonify([e.to_dict() for e in result])
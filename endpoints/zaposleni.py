from flask import Blueprint
from flask import jsonify
from flask import request
from flask import make_response

from sqlalchemy import func
from sqlalchemy import distinct
from sqlalchemy import desc
from sqlalchemy import or_
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc     import DataError
from sqlalchemy.exc     import IntegrityError

from models.mdszadatak import database
from models.mdszadatak import Employee

zaposleni_bp = Blueprint("zaposleni", __name__, url_prefix="/zaposleni")

@zaposleni_bp.route("/", methods=["GET", "POST", "PUT", "DELETE"])
def crud():
	if request.method == "GET":
		id        = None if "id" not in request.args else request.args["id"]
		firstname = None if "firstname" not in request.args else request.args["firstname"]
		lastname  = None if "lastname" not in request.args else request.args["lastname"]
		username  = None if "username" not in request.args else request.args["username"]
		email     = None if "email" not in request.args else request.args["email"]
		salary    = None if "salary" not in request.args else request.args["salary"]

		result = Employee.query.filter(
			or_(Employee.id == id, id == None),
			or_(Employee.firstname == firstname, firstname == None),
			or_(Employee.lastname == lastname, lastname == None),
			or_(Employee.username == username, username == None),
			or_(Employee.email == email, email == None),
			or_(Employee.salary == salary, salary == None)
		).all()
		if len(result) == 0:
			return "", 204
		return [i.to_dict() for i in result], 200
	if request.method == "POST":
		firstname = None if "firstname" not in request.json else request.json["firstname"]
		lastname  = None if "lastname" not in request.json else request.json["lastname"]
		username  = None if "username" not in request.json else request.json["username"]
		email     = None if "email" not in request.json else request.json["email"]
		salary    = None if "salary" not in request.json else request.json["salary"]
		if None in [firstname, lastname, username, email, salary]:
			return "", 400 # Bad Request
		try:
			newEmployee = Employee(
				firstname = firstname,
				lastname = lastname,
				username = username,
				email = email,
				salary = salary
			)
			database.session.add(newEmployee)
			database.session.commit()
			return "", 201
		except DataError:
			return "", 400
		except IntegrityError:
			return "", 409 # Conflict username
	if request.method == "PUT":
		id        = None if "id" not in request.json else request.json["id"]
		firstname = None if "firstname" not in request.json else request.json["firstname"]
		lastname  = None if "lastname" not in request.json else request.json["lastname"]
		username  = None if "username" not in request.json else request.json["username"]
		email     = None if "email" not in request.json else request.json["email"]
		salary    = None if "salary" not in request.json else request.json["salary"]

		if id == None:
			return "", 400
		try:
			employee = Employee.query.filter(Employee.id == id).one()
			employee.firstname = employee.firstname if firstname == None else firstname
			employee.lastname  = employee.lastname if lastname == None else lastname
			employee.username  = employee.username if username == None else username
			employee.email     = employee.email if email == None else email
			employee.salary    = employee.salary if salary == None else salary

			database.session.commit()

			return employee.to_dict(), 200
		except NoResultFound:
			return "", 404
		except DataError:
			return "", 400
		except IntegrityError:
			return "", 409 # Conflict username
	if request.method == "DELETE":
		id = None if "id" not in request.json else request.json["id"]
		if id == None:
			return "", 400
		try:
			employee = Employee.query.filter(Employee.id == id).one()
			database.session.delete(employee)
			database.session.commit()
			return "", 204 # No Content
		except NoResultFound:
			return "", 404
		except DataError:
			return "", 400

	return "error", 405

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
from flask import Blueprint
from flask import jsonify
from flask import request

import pymysql
import os

import pymysql.cursors

DATABASE_HOST = os.environ["DATABASE_HOST"]
DATABASE_PORT = int(os.environ["DATABASE_PORT"])
DATABASE_USER = os.environ["DATABASE_USER"]
DATABASE_PASS = os.environ["DATABASE_PASS"]

def get_db_connection():
	return pymysql.connect(host=DATABASE_HOST, port=DATABASE_PORT, user=DATABASE_USER, password=DATABASE_PASS, database="mdszadatak")

zaposleni_bp = Blueprint("zaposleni", __name__, url_prefix="/zaposleni")

select_query = """
SELECT id, firstname, lastname, username, email, salary
FROM employee
WHERE
	(firstname = %s OR %s IS NULL) AND
	(lastname = %s OR %s IS NULL) AND
	(username = %s OR %s IS NULL) AND
	(email = %s OR %s IS NULL) AND
	(salary = %s OR %s IS NULL);
"""

@zaposleni_bp.route("/", methods=["GET", "POST", "PUT", "DELETE"])
def crud():
	if request.method == "GET":
		id        = None if "id" not in request.args else request.args["id"]
		firstname = None if "firstname" not in request.args else request.args["firstname"]
		lastname  = None if "lastname" not in request.args else request.args["lastname"]
		username  = None if "username" not in request.args else request.args["username"]
		email     = None if "email" not in request.args else request.args["email"]
		salary    = None if "salary" not in request.args else request.args["salary"]
		connection = get_db_connection()
		cursor = connection.cursor(pymysql.cursors.DictCursor)
		cursor.execute(select_query, (
			firstname, firstname,
			lastname, lastname,
			username, username,
			email, email,
			salary, salary
		))
		result = cursor.fetchall()
		print(result)
	if request.method == "POST":
		firstname = None if "firstname" not in request.json else request.json["firstname"]
		lastname  = None if "lastname" not in request.json else request.json["lastname"]
		username  = None if "username" not in request.json else request.json["username"]
		email     = None if "email" not in request.json else request.json["email"]
		salary    = None if "salary" not in request.json else request.json["salary"]
		if None in [firstname, lastname, username, email, salary]:
			return "", 400 # Bad Request
		
	if request.method == "PUT":
		id        = None if "id" not in request.json else request.json["id"]
		firstname = None if "firstname" not in request.json else request.json["firstname"]
		lastname  = None if "lastname" not in request.json else request.json["lastname"]
		username  = None if "username" not in request.json else request.json["username"]
		email     = None if "email" not in request.json else request.json["email"]
		salary    = None if "salary" not in request.json else request.json["salary"]

		if id == None:
			return "", 400
	if request.method == "DELETE":
		id = None if "id" not in request.json else request.json["id"]
		if id == None:
			return "", 400
		

	return "error", 405

@zaposleni_bp.route("/avg_salary", methods=["GET"])
def avg_salary():
	connection = get_db_connection()
	cursor = connection.cursor()
	query = "SELECT AVG(salary) as avg_salary FROM employee"
	cursor.execute(query)
	result = cursor.fetchone()
	result = float(result[0])
	cursor.close() 
	connection.close()
	return {"avg_salary": result}, 200

@zaposleni_bp.route("/third_highest_salary", methods=["GET"])
def third_highest_salary():
	connection = get_db_connection()
	cursor = connection.cursor()
	query = "SELECT DISTINCT salary FROM employee ORDER BY salary DESC LIMIT 1 OFFSET 2"
	cursor.execute(query)
	result = cursor.fetchone()
	cursor.close() 
	connection.close()
	return {"third_highest": result[0]}, 200

@zaposleni_bp.route("/like_a")
def like_a():
	connection = get_db_connection()
	cursor = connection.cursor()
	query = "SELECT firstname, lastname, username, email, id, salary FROM employee where firstname LIKE \"a%\""
	cursor.execute(query)
	result = cursor.fetchall()
	list = []
	for row in result:
		e = {"firstname": row[0], "lastname": row[1], "username": row[2], "email": row[3], "id":int(row[4]), "salary": int(row[5])}
		list.append(e)
	return list, 200
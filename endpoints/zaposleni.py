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
	(id = %s OR %s IS NULL) AND
	(firstname = %s OR %s IS NULL) AND
	(lastname = %s OR %s IS NULL) AND
	(username = %s OR %s IS NULL) AND
	(email = %s OR %s IS NULL) AND
	(salary = %s OR %s IS NULL);
"""

insert_query = """
INSERT INTO employee (firstname, lastname, username, email, salary)
VALUES (%s, %s, %s, %s, %s);
"""

update_query = """
UPDATE employee
SET firstname = %s, lastname = %s, username = %s, email = %s, salary = %s
WHERE id = %s
"""

delete_query = """
DELETE FROM employee
WHERE id = %s
"""

@zaposleni_bp.route("/", methods=["GET", "POST", "PUT", "DELETE"])
def crud():
	with get_db_connection() as connection:
		with connection.cursor(pymysql.cursors.DictCursor) as cursor:
			if request.method == "GET":
				id        = None if "id" not in request.args else request.args["id"]
				firstname = None if "firstname" not in request.args else request.args["firstname"]
				lastname  = None if "lastname" not in request.args else request.args["lastname"]
				username  = None if "username" not in request.args else request.args["username"]
				email     = None if "email" not in request.args else request.args["email"]
				salary    = None if "salary" not in request.args else request.args["salary"]
				cursor.execute(select_query, (
					id, id,
					firstname, firstname,
					lastname, lastname,
					username, username,
					email, email,
					salary, salary
				))
				result = cursor.fetchall()
				if len(result) == 0:
					return "", 204
				return result, 200
			if request.method == "POST":
				firstname = None if "firstname" not in request.json else request.json["firstname"]
				lastname  = None if "lastname" not in request.json else request.json["lastname"]
				username  = None if "username" not in request.json else request.json["username"]
				email     = None if "email" not in request.json else request.json["email"]
				salary    = None if "salary" not in request.json else request.json["salary"]
				if None in [firstname, lastname, username, email, salary]:
					return "", 400 # Bad Request
				try:
					cursor.execute(insert_query, (firstname, lastname, username, email, salary))
					connection.commit()
					print(cursor.fetchall())
				except pymysql.err.IntegrityError:
					return "", 409 # Conflict
				except pymysql.err.DataError:
					return "", 400 # Bad Request
				
			if request.method == "PUT":
				id = None if "id" not in request.json else request.json["id"]
				if id == None:
					return "", 400
				
				try:
					cursor.execute(select_query, (
						id, id,
						None, None,
						None, None,
						None, None,
						None, None,
						None, None
					))
					employee = cursor.fetchone()
					if employee is None:
						return "", 404 # Not Found
					firstname = employee["firstname"] if "firstname" not in request.json else request.json["firstname"]
					lastname  = employee["lastname"] if "lastname" not in request.json else request.json["lastname"]
					username  = employee["username"] if "username" not in request.json else request.json["username"]
					email     = employee["email"] if "email" not in request.json else request.json["email"]
					salary    = employee["salary"] if "salary" not in request.json else request.json["salary"]
					cursor.execute(update_query, (firstname, lastname, username, email, salary, id))
					connection.commit()

					return employee, 200
				except pymysql.err.IntegrityError:
					return "", 409 # Conflict
				except pymysql.err.DataError:
					return "", 400 # Bad Request
			if request.method == "DELETE":
				id = None if "id" not in request.json else request.json["id"]
				if id == None:
					return "", 400
				try:
					cursor.execute(select_query, (
						id, id,
						None, None,
						None, None,
						None, None,
						None, None,
						None, None
					))
					employee = cursor.fetchone()
					if employee is None:
						return "", 404 # Not Found
					cursor.execute(delete_query, (id))
					connection.commit()
					return "", 204 # No Content
				except pymysql.err.IntegrityError:
					return "", 409 # Conflict
				except pymysql.err.DataError:
					return "", 400 # Bad Request

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
	query = "SELECT firstname, lastname, username, email, id, salary FROM employee WHERE firstname LIKE \"a%\""
	cursor.execute(query)
	result = cursor.fetchall()
	list = []
	for row in result:
		e = {"firstname": row[0], "lastname": row[1], "username": row[2], "email": row[3], "id":int(row[4]), "salary": int(row[5])}
		list.append(e)
	return list, 200
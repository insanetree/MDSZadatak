from flask import Blueprint
from flask import jsonify

import pymysql
import os

DATABASE_HOST = os.environ["DATABASE_HOST"]
DATABASE_PORT = int(os.environ["DATABASE_PORT"])
DATABASE_USER = os.environ["DATABASE_USER"]
DATABASE_PASS = os.environ["DATABASE_PASS"]

def get_db_connection():
	return pymysql.connect(host=DATABASE_HOST, port=DATABASE_PORT, user=DATABASE_USER, password=DATABASE_PASS, database="mdszadatak")

zaposleni_bp = Blueprint("zaposleni", __name__, url_prefix="/zaposleni")

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
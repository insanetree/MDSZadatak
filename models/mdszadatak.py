from flask_sqlalchemy import SQLAlchemy

database = SQLAlchemy()

class Employee(database.Model):
	__tablename__ = "employee"

	id        = database.Column("id", database.Integer, primary_key=True)
	firstname = database.Column("firstname", database.String(20), nullable=False)
	lastname  = database.Column("lastname", database.String(20), nullable=False)
	username  = database.Column("username", database.String(20), nullable=False)
	email     = database.Column("email", database.String(50), nullable=False)
	salary    = database.Column("salary", database.Integer, nullable=False)

	def to_dict(self):
		return {
			"id": self.id,
			"firstname": self.firstname,
			"lastname": self.lastname,
			"username": self.username,
			"email": self.email,
			"salary": self.salary
		}

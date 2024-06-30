import pymysql
import pandas as pd

connection = pymysql.connect(
	host="localhost",
	port=3306,
	user="root",
	password="root",
	database="mdszadatak"
)

cursor = connection.cursor()

file = "zaposleni.xlsx"

insert_query = """
INSERT INTO employee (firstname, lastname, username, email, salary)
VALUES (%s, %s, %s, %s, %s)
"""

df = pd.read_excel(file)
for _,i in df.iterrows():
	cursor.execute(insert_query, (i["First Name"], i["Last Name"], i["Username"], i["Email"], int(i["Plata"])))

connection.commit()
cursor.close()
connection.close()
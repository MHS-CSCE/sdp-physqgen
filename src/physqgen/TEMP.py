#importing module
import sqlite3

#connecting to sqlite3
db = sqlite3.connect('example.db')

#creating a cursor object
cursor = db.cursor()

#dropping STUDENT table if it already exists
cursor.execute("DROP TABLE IF EXISTS STUDENT")

#creating columns + their data type
sql = '''CREATE TABLE STUDENT(
    FIRST_NAME CHAR(20) NOT NULL,
    LAST_NAME CHAR(20), 
    EMAIL_A CHAR(30),
    NUMBER_TRIES INT,
    CORRECT BOOL,
    ANSWER FLOAT,
    FORMULA_TYPE CHAR(20),
    DISPLACEMENT INT,
    INITIAL_VELOCITY INT,
    FINAL_VELOCITY INT,
    TIME INT,
    ACCELERATION INT
)'''

cursor.execute(sql)

print("Table created successfully...")

#committing changes to the table
db.commit()

#close connection
db.close()
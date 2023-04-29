from itertools import islice
from sqlalchemy.dialects import sqlite
from sqlalchemy import create_engine

DB_URL = "sqlite:////Users/igor/Documents/School/PPY/CarService1.2/My_package/database/my.db"

engine = create_engine(DB_URL, connect_args={"check_same_thread": False})
connection = engine.connect()

query = """
CREATE TABLE users (
    idUser INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    first_name VARCHAR(32),
    last_name VARCHAR(32)
)
"""

connection.exec_driver_sql(query)
connection.exec_driver_sql(
    "INSERT INTO users (first_name, last_name) VALUES ('a', 'b')"
)

xs = connection.exec_driver_sql("SELECT * FROM users")
print(list(islice(xs, 10)))


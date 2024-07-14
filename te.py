import sqlite3

con = sqlite3.connect("bytegenie_takehome.db")
output = con.execute("select count(*) from events;")
print(type(output.fetchall()))
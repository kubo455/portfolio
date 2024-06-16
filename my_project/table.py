import sqlite3

conn = sqlite3.connect('my_project/database.db')
print("Connected to database succsefully!!!")

# conn.execute('CREATE TABLE users (id INTEGER PRIMARY KEY,username TEXT,password TEXT, balance INTEGER)')
# conn.execute('CREATE TABLE expences (user_id INTEGER, expence_type TEXT, amount REAL, date DATE)')
# conn.execute('CREATE TABLE wallet (user_id INTEGER, income INT, date DATE, new_balance INT)')
conn.execute('CREATE TABLE user_budget (user_id INTEGER, sum INTEGER, goal TEXT)')
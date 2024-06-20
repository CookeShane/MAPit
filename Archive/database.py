# database.py
#
# Author: Shane Cooke
# Date Created: 25/3/2024
# Description: 

import sqlite3

#
# Default Database Class Inherited by all Databases
# Inputs: db_name, the name of the database the categories table is stored in
#         table_name, the name of the table the SQL queries are to be done to
#
class Database:
    def __init__(self, db_name, table_name):
        self.db_name = db_name
        self.table_name = table_name
        self.conn = None
        self.cursor = None

    def open_connection(self):
        if self.conn is None:
            self.conn = sqlite3.connect(self.db_name)
            self.cursor = self.conn.cursor()
        
    def close_connection(self):
        if self.conn is not None:
            self.conn.close()
            self.conn = None
            self.cursor = None

    def execute_query(self, query, values=None):
        self.open_connection()
        with self.conn:
            if values:
                self.cursor.execute(query, values)
            else:
                self.cursor.execute(query)
        #self.close_connection()

    def show_all_rows(self):
        self.open_connection()
        query = f"SELECT * FROM {self.table_name}"
        self.execute_query(query)
        return self.cursor.fetchall()
        #self.close_connection()

#
# Class for Categories Database
# All categories will be stored in this database
# Inherits from Database class
# Inputs: db_name, the name of the database the categories table is stored in
#
class CategoriesDB(Database):
    table_name = 'Categories'

    def __init__(self, db_name):
        self.db_name = db_name
        super().__init__(self.db_name, self.table_name)
        self.create_table()
        self.insert_default_categories()

    def create_table(self):
        query = f"""CREATE TABLE IF NOT EXISTS {self.table_name} (
                    cat_id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL UNIQUE,
                    type TEXT NOT NULL
                )"""
        self.execute_query(query)

    def insert_default_categories(self):
        default_cats = [{'name': 'Salary', 'type': 'Income'},
                        {'name': 'Bonus', 'type': 'Income'},
                        {'name': 'Additional Income', 'type': 'Income'},
                        {'name': 'Rent', 'type': 'Expenses'},
                        {'name': 'Utilities', 'type': 'Expenses'},
                        {'name': 'Daily Travel', 'type': 'Expenses'},
                        {'name': 'Food & Coffee', 'type': 'Expenses'},
                        {'name': 'Subscriptions', 'type': 'Expenses'},
                        {'name': 'Clothes', 'type': 'Expenses'},
                        {'name': 'Social', 'type': 'Expenses'},
                        {'name': 'Presents', 'type': 'Expenses'},
                        {'name': 'Flights', 'type': 'Expenses'},
                        {'name': 'Holiday - Spending', 'type': 'Expenses'},
                        {'name': 'Body Care & Medicine', 'type': 'Expenses'},
                        {'name': 'Emergency Fund', 'type': 'Savings'},
                        {'name': 'Stocks', 'type': 'Savings'},
                        {'name': 'Holiday - Saving', 'type': 'Savings'}]
        
        for cat in default_cats:
            self.insert_category(cat)
        
    def insert_category(self, values):
        query = f"INSERT INTO {self.table_name} (name, type) VALUES (:name, :type)"
        self.execute_query(query, values)
    
    def delete_category(self, name):
        query = f"DELETE from {self.table_name} WHERE name = :name"
        self.execute_query(query, name)

#
# Class for Transactions Database
# All transactions will be stored in this database
# Inherits from Database class
# Inputs: db_name, the name of the database the transactions table is stored in
#
class TransactionsDB(Database):
    table_name = 'Transactions'

    def __init__(self, db_name):
        self.db_name = db_name
        super().__init__(self.db_name, self.table_name)
        self.create_table()

    def create_table(self):
        query = f"""CREATE TABLE IF NOT EXISTS {self.table_name} (
                    trans_id INTEGER PRIMARY KEY,
                    date TEXT NOT NULL,
                    type TEXT NOT NULL,
                    cat_id INTEGER NOT NULL,
                    amount REAL NOT NULL,
                    reoccur INTEGER NOT NULL,
                    details TEXT,
                    FOREIGN KEY (cat_id) REFERENCES Categories(cat_id)
                )"""
        self.execute_query(query)
        
    def insert_transaction(self, values):
        query = f"INSERT INTO {self.table_name} (date, type, cat_id, amount, reoccur, details) VALUES (:date, :type, :cat_id, :amount, :reoccur, :details)"
        self.execute_query(query, values)
    
    def delete_transaction(self, id):
        query = f"DELETE from {self.table_name} WHERE trans_id = :id"
        self.execute_query(query, id)

#
# Class for Planner Database
# The monthly planned amount per category will be stored in this database
# Inherits from Database class
# Inputs: db_name, the name of the database the transactions table is stored in
#
class PlannerDB(Database):
    table_name = 'Planner'

    def __init__(self, db_name):
        self.db_name = db_name
        super().__init__(self.db_name, self.table_name)
        self.create_table()

    def create_table(self):
        query = f"""CREATE TABLE IF NOT EXISTS {self.table_name} (
                    plan_id INTEGER PRIMARY KEY,
                    cat_id INTEGER NOT NULL,
                    year INTEGER NOT NULL,
                    month INTEGER NOT NULL,
                    amount REAL NOT NULL,
                    FOREIGN KEY (cat_id) REFERENCES Categories(cat_id)
                )"""
        self.execute_query(query)
        
    def insert_planned_amount(self, values):
        query = f"INSERT INTO {self.table_name} (cat_id, year, month, amount) VALUES (:cat_id, :year, :month, :amount)"
        self.execute_query(query, values)
    
    def delete_planned_amount(self, values):
        query = f"DELETE from {self.table_name} WHERE (cat_id, year, month) = (:cat_id, :year, :month)"
        self.execute_query(query, values)

#
# Banks Database
#
# class BankDB(Database):
#     table_name = 'Banks'

#     def __init__(self):
#         super().__init__(self.table_name)
#         self.create_table()
#         self.insert_default_banks()

#     def create_table(self):
#         query = f"""CREATE TABLE IF NOT EXISTS {self.table_name} (
#                     id INTEGER PRIMARY KEY,
#                     name TEXT NOT NULL UNIQUE
#                 )"""
#         self.execute_query(query)

#     def insert_default_banks(self):
#         default_banks = [{'name': 'Revolut'},
#                         {'name': 'PTSB'},
#                         {'name': 'Cash'}]
        
#         for bank in default_banks:
#             self.insert_bank(bank)
        
#     def insert_bank(self, values):
#         query = f"INSERT INTO {self.table_name} (name) VALUES (:name)"
#         self.execute_query(query, values)
    
#     def delete_bank(self, name):
#         query = f"DELETE from {self.table_name} WHERE name = :name"
#         self.execute_query(query, name)
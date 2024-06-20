# main.py

from database import CategoriesDB, TransactionsDB, PlannerDB

if __name__ == "__main__":
    database_name = ':memory:'

    categories = CategoriesDB(':memory:')
    print(categories.show_all_rows())

    transactions = TransactionsDB(':memory:')
    print(transactions.show_all_rows())

    planned_amounts = PlannerDB(':memory:')
    print(planned_amounts.show_all_rows())
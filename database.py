import sqlite3

# tables
CREATE_COINS_TABLE = """CREATE TABLE IF NOT EXISTS coins (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE, 
    quantity REAL,
    price REAL DEFAULT 0.00,
    value REAL GENERATED ALWAYS AS (quantity * price)
);"""

# query statements
INSERT_COINS = "Insert INTO coins (name, quantity) VALUES (?, ?);"
GET_ALL_COINS = "SELECT * FROM coins ORDER BY name ASC;"
GET_COIN_BY_NAME = "SELECT * FROM coins WHERE name = ?;"
GET_VALUE_SUM = "SELECT TOTAL (value) FROM coins;"
UPDATE_COIN_QUANTITY = "UPDATE coins SET quantity = ? WHERE name = ?;"
UPDATE_COIN_PRICE = "UPDATE coins SET price = ? WHERE name = ?;"
DELETE_COIN = "DELETE FROM coins WHERE name = ?;"

def connect():
    return sqlite3.connect("portfolio.db")

def create_tables(connection):
    with connection:
        connection.execute(CREATE_COINS_TABLE)

def add_coin(connection, name, quantity):
    with connection:
        connection.execute(INSERT_COINS, (name, quantity))

def get_all_coins(connection):
    with connection:
        return connection.execute(GET_ALL_COINS).fetchall()

def get_value_sum(connection):
    with connection:
        return connection.execute(GET_VALUE_SUM).fetchone()

def get_coin_by_name(connection, name):
    with connection:
        return connection.execute(GET_COIN_BY_NAME, (name,)).fetchone()

def update_coin_quantity(connection, quantity, name):
    with connection:
        connection.execute(UPDATE_COIN_QUANTITY, (quantity, name))
    
def update_coin_price(connection, price, name):
    with connection:
        connection.execute(UPDATE_COIN_PRICE, (price, name))

def delete_coin(connection, name):
    with connection:
        connection.execute(DELETE_COIN, (name,))
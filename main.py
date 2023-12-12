# python
import os
import time
# local
import database
# pip
import requests
from tabulate import tabulate

# Constants
CLEAR_AND_RETURN = "\033[H"
GREEN_FONT = "\033[32m"
YELLOW_FONT = "\033[93m"
RESET_FONT = "\033[0m"

DISPLAY_NAME = """
   _____ _______     _______ _______ ____  
  / ____|  __ \ \   / /  __ \__   __/ __ \ 
 | |    | |__) \ \_/ /| |__) | | | | |  | |
 | |    |  _  / \   / |  ___/  | | | |  | |
 | |____| | \ \  | |  | |      | | | |__| |
  \_____|_|  \_\ |_|  |_|      |_|  \____/ 
                                                                                 
"""
                                                                                                                               
MENU_PROMPT = """
--------------------
        Menu      
--------------------

(1) View Portfolio
(2) Add Coin
(3) Update Quantity
(4) Delete Coin
(5) Exit

=> Select [1-5]: """

# ----------------------------------- CLEAR SCREEN -----------------------------------
def clear_screen():
    os.system("clear")

# ----------------------------------- ON START -----------------------------------
def main():
    clear_screen()
    # connect to db and create table 'coins' if does not exist
    connection = database.connect()
    database.create_tables(connection)

    print(DISPLAY_NAME)

    # display menu options
    menu(connection)

# ----------------------------------- MENU -----------------------------------
def menu(connection):
    user_input = input(MENU_PROMPT)

    if user_input == "1":
        fetch_prices(connection)
    elif user_input == "2":
        add_coin(connection)
    elif user_input == "3":
        edit_quantity(connection)
    elif user_input == "4":
        delete_coin(connection)
    else:
        quit(DISPLAY_NAME)

# ----------------------------------- API -----------------------------------
def fetch_prices(connection):
    coin_list = ""
    coins = database.get_all_coins(connection)
    for coin in coins:
        coin_list += f"{coin[1]}%2C" # append coin name to coin list
    
    COINGECKO_URL = f"https://api.coingecko.com/api/v3/simple/price?ids={coin_list}&vs_currencies=usd"

    # make get request to api
    response = requests.get(COINGECKO_URL)
    # store response in JSON_DATA 
    JSON_DATA = response.json()
    # loop through JSON data
    for coin_name in JSON_DATA: 
        price = JSON_DATA[coin_name]["usd"]
        database.update_coin_price(connection, price, coin_name)
    
    # display menu
    view_portfolio(connection)

# ----------------------------------- READ -----------------------------------
def view_portfolio(connection):
    clear_screen()

    coins = database.get_all_coins(connection)
    total = database.get_value_sum(connection)

    table_data = [] # create empty list
    for coin in coins:
        row = []
        name, quantity, price, value = coin[1], coin[2], coin[3], coin[4]
        percent = (value / total[0]) * 100
        # extend appends multiple values to a list
        row.extend([
            name, 
            "{0:.4f}".format(quantity), 
            "{0:.2f}".format(price), 
            "{0:.2f}".format(value),
            "{0:.1f}".format(percent),
        ]) 
        table_data.append(row)

    # column headers
    titles = ["Name", "Quantity", "Price", "Value", "Percent"]
    # column alignment
    align = ["left", "right", "right", "right", "center"]

    if len(coins) == 0:
        print(tabulate(table_data, headers=titles, tablefmt="simple_grid"))
    else:
        table_data.append(["", "", "TOTAL", "{0:.2f}".format(total[0]), ""])
        print(tabulate(table_data, headers=titles, tablefmt="simple_grid", colalign=align))

    # display menu & pass database connection
    print("")
    menu(connection)

# ----------------------------------- CREATE -----------------------------------
def add_coin(connection):
    clear_screen()

    print(DISPLAY_NAME)

    user_input = input("=> Enter coin name to add [ex: bitcoin]: ").lower()
    COINGECKO_URL = f"https://api.coingecko.com/api/v3/coins/{user_input}"

    # make get request to api
    response = requests.get(COINGECKO_URL)

    # confirm user input is a valid coin name
    if response.status_code != 200:
        # print error message and return to menu
        clear_screen()
        print(f"{YELLOW_FONT}# {user_input} not found... enter coin's API id from 'coingecko.com'{RESET_FONT}")
        print("")
        menu(connection)

    clear_screen()
    print(DISPLAY_NAME)
 
    while True:
        try:
            quantity = float(input(f"=> Enter quantity of {user_input}: "))
            break
        except ValueError:
            clear_screen()
            print(DISPLAY_NAME)
            print(f"{YELLOW_FONT}# Enter a valid quantity [ex 17.248]{RESET_FONT}")
            print("")
    
    clear_screen()

    # add coin to database
    database.add_coin(connection, user_input, quantity)

    clear_screen()
    print(DISPLAY_NAME)
    print(f"{GREEN_FONT}# {user_input} added to portfolio{RESET_FONT}")
    print("")
    
    menu(connection)

# ----------------------------------- UPDATE -----------------------------------
def edit_quantity(connection):
    clear_screen()

    print(DISPLAY_NAME)

    user_input = input("Enter coin name to update quantity: ").lower()
    coin = database.get_coin_by_name(connection, user_input)
    if coin:
        clear_screen()
        print(DISPLAY_NAME)
        new_quantity = float(input(f"Enter new quantity for {user_input}: "))
        # update database
        database.update_coin_quantity(connection, new_quantity, user_input)
        # print success message
        clear_screen()
        print(DISPLAY_NAME)
        print(f"{GREEN_FONT}# quantity for {user_input} updated{RESET_FONT}")
    else:
        # print error message
        clear_screen()
        print(DISPLAY_NAME)
        print(f"{YELLOW_FONT}# {user_input} not found. Back to main menu{RESET_FONT}")
    
    menu(connection)

# ----------------------------------- DELETE -----------------------------------
def delete_coin(connection):
    clear_screen()

    print(DISPLAY_NAME)

    user_input = input("Enter coin name to delete: ").lower()
    coin = database.get_coin_by_name(connection, user_input)
    if coin:
        clear_screen()
        # delete from database
        database.delete_coin(connection, user_input)
        # print success message
        print(DISPLAY_NAME)
        print(f"{GREEN_FONT}# {user_input.lower()} deleted{RESET_FONT}")
    else:
        # print error message
        clear_screen()
        print(DISPLAY_NAME)
        print(f"{YELLOW_FONT}# {user_input.lower()} not found. Back to main menu{RESET_FONT}")
    
    menu(connection)

# ----------------------------------- EXIT -----------------------------------
def quit(message):
    clear_screen()
    time_elasped = 0
    seconds = 2

    while time_elasped < seconds:
        time.sleep(1)
        time_elasped += 1

        time_remaining = seconds - time_elasped
        print(f"{CLEAR_AND_RETURN}{GREEN_FONT}{message}{RESET_FONT}\n \nExiting in: {time_remaining} seconds")
    
    clear_screen()

# ----------------------------------- RUN SCRIPT -----------------------------------
if __name__ == "__main__":
    main()
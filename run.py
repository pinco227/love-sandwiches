import gspread
from google.oauth2.service_account import Credentials
from pprint import pprint

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
]
CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('love_sandwiches')
SALES = SHEET.worksheet('sales')
SURPLUS = SHEET.worksheet('surplus')
STOCK = SHEET.worksheet('stock')


def get_sales_data():
    """
    Get sales figures input from the user.
    Run a while loop to collect a valid string of data from the user
    via the terminal, which must pe a string of 6 numbers separated
    by comma. The loop will repeatedly request data, until is valid.
    """

    while True:
        print("Please enter sales data from the last market.")
        print("Data should be six numbers, separated by commas.")
        print("Example: 10,20,30,40,50,60\n")

        data_str = input("Enter your data here: ")

        sales_data = data_str.split(",")

        if validate_data(sales_data):
            print("Data is valid!")
            break

    return validate_data(sales_data)


def validate_data(values):
    """
    Inside the try, converts all string values to integers.
    Raises ValueError if strings cannot be converted into int,
    or if there aren't exactly 6 values
    """

    try:
        [int(value) for value in values]
        if len(values) != 6:
            raise ValueError(
                f"Exactly 6 values required, you provided {len(values)}"
            )
    except ValueError as e:
        print(f"Invalid data: {e}, please try again.\n")
        return False

    return [int(value) for value in values]


def update_worksheet(sheet, data):
    """
    Update sales worksheet, add new row with the list data provided.
    """

    print("Updating sales worksheet...\n")
    sheet.append_row(data)
    print("Sales worksheet updated successfully.\n")


def calculate_surplus_data(sales_row):
    """
    Compare sales with stock and calculate the surplus for each item type.
    The surplus is defined on the sales figure substracted from the stock:
    - Positive surplus indicates wast
    - Negative surplus indicates extra made when stock was sold out.
    """

    print("Calculating surplus data...\n")
    stock = STOCK.get_all_values().pop()
    pprint(stock)


def main():
    """
        Run all program functions
    """
    data = get_sales_data()
    update_worksheet(SALES, data)
    calculate_surplus_data(data)


print("Welcome to Love Sandwiches Data Automation\n")
main()

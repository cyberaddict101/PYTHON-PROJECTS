import re
import sqlite3

conn = sqlite3.connect('CryptoTrading.db')
cursor = conn.cursor()

def username_recall():
    sql_select = f"SELECT user_name FROM Registered_members"
    cursor.execute(sql_select)
    username_result = cursor.fetchall()
    return [username_result[i][0] for i in  range(len(username_result))]

def username_balance_check(username):
    sql_select = f'SELECT wallet_balance FROM Registered_members WHERE user_name =  "{username}"'
    cursor.execute(sql_select)
    username_balance = cursor.fetchall()
    if len(username_balance) == 1:
        return username_balance[0][0]
    else:
        return username_balance


def username_walletbalance_update(username, deposit_amount):
    cursor.execute(f"UPDATE Registered_members SET wallet_balance = wallet_balance +"
                   f" {deposit_amount} WHERE user_name = '{username}'")
    conn.commit()


def username_key_recall(username):
    sql_select = f'SELECT key FROM Registered_members WHERE user_name= "{username}"'
    cursor.execute(sql_select)
    key_result = cursor.fetchall()
    return key_result[0][0]


def username_uid_recall(username):
    sql_select = f'SELECT user_id FROM Registered_members WHERE user_name= "{username}"'
    cursor.execute(sql_select)
    user_id = cursor.fetchall()[0][0]
    return user_id


#   email based functions
def email_recall():
    sql_select = 'SELECT email_address FROM Registered_members'
    cursor.execute(sql_select)
    email_result = cursor.fetchall()
    return [email_result[i][0] for i in  range(len(email_result))]


def email_key_recall(email):
    sql_select = f'SELECT key FROM Registered_members WHERE email_address= "{email}"'
    cursor.execute(sql_select)
    key_result = cursor.fetchall()
    return key_result[0][0]


def email_balance_check(email):
    sql_select = f'SELECT wallet_balance FROM Registered_members WHERE email_address = "{email}"'
    cursor.execute(sql_select)
    email_balance = cursor.fetchall()
    if len(email_balance) == 1:
        return email_balance[0][0]
    else:
        return email_balance


def email_username(email):
    sql_select = f'SELECT user_name FROM Registered_members WHERE email_address = "{email}"'
    cursor.execute(sql_select)
    username = cursor.fetchall()
    username = username[0][0]
    return username


def email_userid_recall(email):
    sql_select = f'SELECT user_id FROM Registered_members WHERE email_address = "{email}"'
    cursor.execute(sql_select)
    e_user_id = cursor.fetchall()[0][0]
    return e_user_id


def userid_trans():
    sql_select = f"SELECT user_id FROM transaction_history"
    cursor.execute(sql_select)
    userid_trans = cursor.fetchall()
    if len(userid_trans) < 1:
        return userid_trans
    else:
        return [userid_trans[i - 1][0] for i in range(len(userid_trans))]


def email_walletbalance_update(email, deposit_amount):
    cursor.execute(f"UPDATE Registered_members SET wallet_balance = wallet_balance +"
                   f" {deposit_amount} WHERE email_address = '{email}'")
    conn.commit()


#   Regular expression functions

def name_check(name):
    pattern = r"^[aA-zZ]+[\-\.]?\s?[aA-zZ]+$"
    match = re.search(pattern, name)
    if match:
        return ['match']
    else:
        return ['no match']


def email_check(email):
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'  # work on the email regex
    if re.fullmatch(regex, email):
        return ["valid email"]
    else:
        return ["invalid email"]


def phone_num_check(phone_num):
    pattern = r"^((0[7-9][0-1])|(\+234[7-9][0-1]))\d{8}$"
    match = re.search(pattern, phone_num)
    if match:
        return ["valid mobile number"]
    else:
        return ["invalid mobile number"]


def amount_validation(amount):
    pattern = r"^[^\d]+(.+)?$"
    match = re.search(pattern, amount)
    if match:
        return ["invalid entry"]
    else:
        return ["valid entry"]


def first_deposit_amount_check(amount):
    pattern = r"^(1[0-9][0-9][0-9])+|([2-9][0-9][0-9]+\.?[0-9]*)$"
    match = re.search(pattern, amount)
    if match:
        return ["not below 200"]
    else:
        return ["below 200"]

#modified to accept between 30 to <100%
def percentage_return_input_test(percentage):
    pattern = r"^([3-9]\d)|([3-9]\d\.\d+)$"
    match = re.fullmatch(pattern, percentage)
    if match:
        return "valid entry"
    else:
        return "invalid entry"

#modified to check number pattern
def trade_duration_match(option):
    pattern = r"[1-3]"
    match = re.fullmatch(pattern, option)
    if match:
        return 'VALID INPUT'
    else:
        return 'INVALID INPUT'

def trade_pair_validation(trade_pair):
    pattern = r'[A-C]'
    match = re.fullmatch(pattern,trade_pair)
    if match:
        return "VALID INPUT"
    else:
        return  "INVALID INPUT"

def trade_direction_validation(option_direction):
    pattern = r'[A-B]'
    match = re.fullmatch(pattern,option_direction)
    if match:
        return "VALID OPTION"
    else:
        return  "INVALID OPTION"


#   CREATE TABLE FUNCTIONS

def reg_member_table():
    # cursor.execute('DROP TABLE IF EXISTS Registered_members')
    cursor.execute(
        'CREATE TABLE IF NOT EXISTS Registered_members(user_id INTEGER PRIMARY KEY,first_name VARCHAR NOT NULL, '
        'last_name VARCHAR NOT NULL,email_address NVARCHAR NOT NULL, user_name NVARCHAR UNIQUE NOT NULL, '
        'key NVARCHAR NOT NULL, phone_num CHAR NOT NULL, wallet_balance FLOAT NOT NULL DEFAULT 0.00, '
        'reg_date DATE)')
    conn.commit()


def trans_hist_table():
    # cursor.execute('DROP TABLE IF EXISTS transaction_history')
    cursor.execute('CREATE TABLE IF NOT EXISTS transaction_history(tran_hist_id INTEGER PRIMARY KEY,user_id INTEGER,'
                   'transaction_type VARCHAR  NOT NULL CHECK(transaction_type IN("deposit","withdrawal")),'
                   'amount MONEY NOT NULL, transaction_date DATETIME, transaction_time TEXT)')
    conn.commit()


def trading_hist_table():
    # cursor.execute('DROP TABLE IF EXISTS trading_history')
    cursor.execute('CREATE TABLE IF NOT EXISTS trading_history(trade_id INTEGER PRIMARY KEY,user_id INTEGER,'
                   'trade_pair VARCHAR  NOT NULL CHECK(trade_pair IN("USD/BTC","EURO/BTC","ETH/BTC")),'
                   'trade_option CHAR  NOT NULL CHECK(trade_option IN("rise","fall")), trade_percent INTEGER,'
                   'trade_amount MONEY NOT NULL, date DATETIME, trade_start_time TEXT,start_price, end_price,'
                   ' trade_end_time TEXT, trade_result CHAR, '
                   'result_amount MONEY)')
    conn.commit()

def insert_trade_details(user_id, trade_pair, trade_option, trade_percent, trade_amount, date_now, start_time,
                                  start_price,end_price, end_time,trade_result, result_amount):
    cursor.execute("INSERT INTO trading_history(user_id, trade_pair, trade_option, trade_percent,trade_amount,"
					"date, trade_start_time, start_price, end_price, trade_end_time,trade_result, result_amount) "
					"VALUES (?,?,?,?,?,?,?,?,?,?,?,?)", (user_id, trade_pair, trade_option, trade_percent, trade_amount, date_now, start_time,
                                                 start_price,end_price, end_time,trade_result, result_amount))
    conn.commit()

def trade_wallet_balance_update(wallet_balance,user_id):
    cursor.execute("UPDATE Registered_members SET wallet_balance =(?) WHERE user_id = (?)",(wallet_balance,user_id))
    conn.commit()
#   ENCODING PASSWORD

def encode_password(password):
    encoded = []
    alphabet = 'abcdefghijklmnopqrstuvwxyz'
    key = 'xznlwebgjhqdyvtkfuompciasr'
    password = password.lower()
    for c in password:
        if c.isalpha():
            encoded.append(key[alphabet.index(c)])
        else:
            encoded.append(c)
    str_encoded = ''
    for c in encoded:
        str_encoded += c
    return str_encoded

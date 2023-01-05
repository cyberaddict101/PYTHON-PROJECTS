import sqlite3
import re

conn = sqlite3.connect('CryptoTrading.db')
cursor = conn.cursor()


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
    return key_result


def username_uid_recall(username):
    sql_select = f'SELECT user_id FROM Registered_members WHERE user_name= "{username}"'
    cursor.execute(sql_select)
    user_id = cursor.fetchall()[0][0]
    return user_id



#   email based functions
def email_recall():
    sql_select = 'SELECT email_address FROM Registered_members'
    cursor.execute(sql_select)
    email_result =cursor.fetchall()
    return email_result


def email_key_recall(email):
    sql_select = f'SELECT key FROM Registered_members WHERE email_address= "{email}"'
    cursor.execute(sql_select)
    key_result = cursor.fetchall()
    return key_result


def email_balance_check(email):
    sql_select = f'SELECT wallet_balance FROM Registered_members WHERE email_address = "{email}"'
    cursor.execute(sql_select)
    email_balance = cursor.fetchall()
    if len(email_balance) == 1:
        return email_balance[0][0]
    else:
        return email_balance


def email_username(email):
    e_username = ""
    sql_select = f'SELECT user_name FROM Registered_members WHERE email_address = "{email}"'
    cursor.execute(sql_select)
    username = cursor.fetchall()
    for i in range(len(username[0])):
        e_username += username[0][i-1]
    return e_username



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
        return [userid_trans[i-1][0] for i in range(len(userid_trans))]

def email_walletbalance_update(email, deposit_amount):
    cursor.execute(f"UPDATE Registered_members SET wallet_balance = wallet_balance +"
                   f" {deposit_amount} WHERE email_address = '{email}'")
    conn.commit()




#   Regular expression functions

def name_check(name):
    pattern = r"^[aA-zZ]+[\-\.]?\s?[aA-zZ]+$"
    match =re.search(pattern,name)
    if match:
        return ['match']
    else:
        return ['no match']


def email_check(email):
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b' # work on the email regex
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


def percentage_return_input_test(percentage):
    pattern = r"^(90|[3-8]\d)|([3-8]\d\.\d+)$"
    match = re.fullmatch(pattern,percentage)
    if match:
        return "valid entry"
    else:
        return "invalid entry"

def trade_option_match(option):
    pattern = r"[A-C]"
    match = re.fullmatch(pattern, option)
    if match:
        return 'VALID INPUT'
    else:
        return 'INVALID INPUT'

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



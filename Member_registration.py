# import re
import sqlite3
from project_functions import encode_password
import project_functions
conn = sqlite3.connect('CryptoTrading.db')
cursor = conn.cursor()


project_functions.reg_member_table()
cursor.execute('SELECT user_name FROM Registered_members')
username_result = cursor.fetchall()
# print(username_result)




list_mem_det = []



def member_registration():
    list_mem_det = []
    print("Welcome to teamB crypto trading platform registration page"'\n'
          "Kindly fill out necessary information correctly"'\n'
          "THANK YOU")
    while True:
        fname = input('Enter your first name: '.strip()).title()
        validate_name = project_functions.name_check(fname)
        if validate_name == ['match']:
            print('First name saved!''\n', 'Kindly continue with the registration')
            list_mem_det.append(fname)
            break
        else:
            print('You have not made a valid Entry!')
    while True:
        lname = input('Enter your last name: '.strip()).title()
        validate_name = project_functions.name_check(lname)
        if validate_name == ['match']:
            print('Last name saved!''\n', 'Kindly continue with the registration')
            list_mem_det.append(lname)
            break
        else:
            print('You have made an invalid Entry!')

    while True:
        email = input('Enter your email address: '.strip()).lower()
        validation = project_functions.email_check(email)
        if validation == ['invalid email']:
            print('You have entered an invalid email!')
        else:
            print('Valid email!''\n\n''Email saved!')
            list_mem_det.append(email)
            break
    while True:
        username = input('Enter your desired username: '.lower()).strip() # use regex instead
        if username.isalnum() and username not in [username_result[i][0] for i in range(len(username_result))]:
            print('Username stored! continue with the registration.')  # update username format
            list_mem_det.append(username)
            break
        elif username.isalnum() and username in [username_result[i][0] for i in range(len(username_result))]:
            print('username is already used, kindly choose another username')
        else:
            print('You have not made any valid Entry, an empty space alone does not qualify as a valid entry')
    while True:
        password = encode_password(input('Input your password: ').lower().strip())  # make the encryption stronger
        confirm_password = encode_password(input('Confirm password: ').lower().strip())
        print(confirm_password)
        if 5 >= len(password):
            print('length of password has to be at least six characters long')
        elif password == '':
            print('Enter a valid password')
        elif password == confirm_password:
            print('password has been set!')
            encrypted_password = str(encode_password(password))
            list_mem_det.append(encrypted_password)
            break
    while True:
        phone_number = input('Enter your 11 digits mobile number without spaces: ').strip()
        validate_num = project_functions.phone_num_check(phone_number)
        if validate_num == ["valid mobile number"]:
            print('Phone number has been saved''\n\n''Registration Successful!''\n\n')
            list_mem_det.append(phone_number)
            cursor.execute('INSERT INTO Registered_members(first_name,last_name,email_address,user_name,'
                           'key,phone_num) VALUES (?,?,?,?,?,?)', (fname, lname, email, username, password, phone_number))
            conn.commit()
            break
        else:
            print('Invalid phone number or character entered!''\n'
                  'kindly enter a valid phone number without space in between! ')

"""
use regex to enforce a particular pattern in the username
work on the encryption of password to accommodate uppercase letters and special characters
use regex to enforce the password to include numbers,alphabets(uppercase and lowercase) and special characters.

"""



# member_registration()

#   dont call login function in registration
#   clean up the list and replace with dictionary/werite directly into a file



        # return list_mem_det
    # loadwallet = input('Would you like to load your wallet now?''\n''\n'
    #                    'A.       YES''\n''\n'
    #                    'B.        NO')

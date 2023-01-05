import  datetime
import pytz
import requests
import sqlite3
import Member_registration
import project_functions

project_functions.trans_hist_table()

conn = sqlite3.connect('CryptoTrading.db')
cursor = conn.cursor()



def api_call(coin):
    response = requests.get('https://api.coingecko.com/api/v3/exchange_rates')
    rates_json = response.json()
    return rates_json['rates'][coin]['value']



def mem_login():
    break_loop1 = ''
    break_loop2 = ''
    break_loop3 = ''
    break_loop4 = ''

    while True:
        if break_loop1 == 'B':
            break
        username = input("Enter your username: ").strip().lower()
        password = project_functions.encode_password(input('Enter your password: ').strip().lower())
        username_key_match = project_functions.username_key_recall(username)
        sql_select = f"SELECT user_name FROM Registered_members"
        cursor.execute(sql_select)
        result = cursor.fetchall()
        username_result =result
        if username not in [username_result[i][0] for i in range(len(username_result))]:
            print(f"username {username} does not exist! Kindly choose an option below to proceed")
            while True:
                if break_loop2 =='B':
                    break
                options = input(f"A.   Forgot username but i have registered""\n"
                                f"B.   Take me to registration page!""\n"
                                f"Q    QUIT""\n"
                                f"Select an option from the above: "'\n').upper()
                if options == 'A':
                    while True:
                        if break_loop3 == 'B':
                            break
                        email = input('Enter registered email address: ').strip().lower()
                        email_match = project_functions.email_recall()
                        if email not in [email_match[i-1][0] for i in range(len(email_match))]:
                            print(f'The email provided ({email}), is not associated with any registered account')
                            break
                        else:
                            password = project_functions.encode_password(input('Enter your password: ').lower().strip())
                            email_key_match = project_functions.email_key_recall(email)
                            e_username = project_functions.email_username(email)
                            if password in [email_key_match[i][0] for i in range(len(email_key_match))]:
                                print("Login successful!")
                                while True:
                                    if break_loop4 == 'B':
                                        break
                                    balance = project_functions.email_balance_check(email)
                                    print(f'Welcome {e_username}!"\n"'
                                          f'Your wallet balance is ${balance}'"\n"
                                          f'Here are the current exchange rates of bitcoin :')
                                    usd_rate = api_call('usd')
                                    eth_rate = api_call('eth')
                                    eur_rate = api_call('eur')
                                    print(f'Exchange rate of USD to 1 BTC is {usd_rate}')
                                    print(f'Exchange rate of ETH to 1 BTC is {eth_rate}')
                                    print(f'Exchange rate of EURO to 1 BTC is {eur_rate}')
                                    homepage_options = input("What will you like to do?"'\n'
                                                             "A       Trade"'\n'
                                                             "B       Deposit"'\n'
                                                             "C       Check wallet balance"'\n'
                                                             "Q       Logout"'\n'
                                                             "Select an option: ").upper()
                                    if homepage_options == 'B':
                                        while True:
                                            deposit_amount = input("Enter the amount you wish to deposit: ").strip()
                                            if deposit_amount == "":
                                                print("you have not made any valid entry")
                                            amount_validation = project_functions.amount_validation(deposit_amount)
                                            if amount_validation == ["invalid entry"]:
                                                print("you have made an invalid entry"'\n'
                                                      "Please note that special characters,letters, combination of both special characters and letters"'\n'
                                                      "or the combination any of the previously mentioned with number is not an acceptable input"'\n')
                                            else:
                                                u_deposit_amount = project_functions.first_deposit_amount_check(deposit_amount)
                                                e_user_id = project_functions.email_userid_recall(email)
                                                userid_t = project_functions.userid_trans()
                                                if u_deposit_amount == ["not below 200"] and [e_user_id] not in userid_t:
                                                    print(f"Deposit of ${deposit_amount} successful!")
                                                    project_functions.email_walletbalance_update(email,deposit_amount)
                                                    today = datetime.datetime.now(tz=pytz.timezone('Africa/Lagos'))
                                                    time_now = today.time().strftime('%H:%M:%S')
                                                    date_now = today.date()
                                                    cursor.execute("INSERT INTO transaction_history(user_id, transaction_type, amount, transaction_date, transaction_time) "
                                                                   "VALUES (?,?,?,?,?)", (e_user_id, 'deposit', deposit_amount,date_now,time_now))
                                                    conn.commit()
                                                    break
                                                elif u_deposit_amount == ["not below 200"] and e_user_id in userid_t:
                                                    print(f"Deposit of ${deposit_amount} successful!")
                                                    project_functions.email_walletbalance_update(email,deposit_amount)
                                                    today = datetime.datetime.now(tz=pytz.timezone('Africa/Lagos'))
                                                    time_now = today.time().strftime('%H:%M:%S')
                                                    date_now = today.date()
                                                    cursor.execute("INSERT INTO transaction_history(user_id, transaction_type, amount, transaction_date, transaction_time) "
                                                                   "VALUES (?,?,?,?,?)", (e_user_id, 'deposit', deposit_amount,date_now,time_now))
                                                    conn.commit()
                                                    break
                                                elif u_deposit_amount != ["not below 200"] and e_user_id in userid_t:
                                                    print(f"Deposit of ${deposit_amount} successful!")
                                                    project_functions.email_walletbalance_update(email,deposit_amount)
                                                    today = datetime.datetime.now(tz=pytz.timezone('Africa/Lagos'))
                                                    time_now = today.time().strftime('%H:%M:%S')
                                                    date_now = today.date()
                                                    cursor.execute("INSERT INTO transaction_history(user_id, transaction_type, amount, transaction_date, transaction_time) "
                                                                   "VALUES (?,?,?,?,?)", (e_user_id, 'deposit', deposit_amount,date_now,time_now))
                                                    conn.commit()
                                                    break
                                                else:
                                                    print("Your first ever deposit can not be less than $200!")
                                    elif homepage_options == 'A':
                                        while True:
                                            options = input("A          EURO/BTC"'\n'
                                                            "B          USD/BTC"'\n'
                                                            "C          ETH/BTC"'\n'
                                                            "Select an option from the above: ").strip().upper()
                                            options_validation = project_functions.trade_option_match(options)
                                            if options_validation == 'INVALID INPUT':
                                                print('You have made an invalid input! Kindly input between A-C')
                                            else:
                                                if options == 'A':
                                                    count1 = 0
                                                    while count1 < 1:
                                                        option_A = input("A     BTC will rise against EURO"'\n'
                                                                         "B     BTC will drop against EURO"'\n'
                                                                         "Select an option above for your prediction: ").strip().upper()
                                                        option_A_validation = project_functions.trade_option_match(option_A)
                                                        if option_A_validation == 'INVALID OPTION':
                                                            print(
                                                                'You have made an invalid input! Kindly input between A-B')
                                                        else:
                                                            count1 += 1
                                                    count2 = 0
                                                    while count2 < 1:
                                                        trading_amount = input(
                                                            'How much will you like to trade?: ').strip()
                                                        trading_amount_validation = project_functions.amount_validation(
                                                            trading_amount)
                                                        if trading_amount_validation == ["invalid entry"]:
                                                            print("you have made an invalid entry"'\n'
                                                                  "Please note that special characters,letters, combination of both special characters and letters"'\n'
                                                                  "or the combination any of the previously mentioned with number is not an acceptable input"'\n')
                                                        else:
                                                            wallet_balance = project_functions.email_balance_check(
                                                                email)
                                                            if trading_amount > wallet_balance:
                                                                print(
                                                                    "you can not stake/trade more than your wallet balance")
                                                            else:
                                                                count2 += 1
                                                    count3 = 0
                                                    while count3 < 1:
                                                        duration_option = input(
                                                            "For how long will you like to trade?"'\n'
                                                            "A      1min"'\n'
                                                            "B      2min"'\n'
                                                            "C      3min"'\n'
                                                            "Select an option : ")
                                                        duration_validation = project_functions.trade_option_match(duration_option)
                                                        if duration_validation == 'INVALID OPTION':
                                                            print(
                                                                'You have made an invalid input! Kindly input between A-C in correspondence to the displayed acceptable duration')
                                                        else:
                                                            count3 += 1
                                                    count4 = 0
                                                    while count4 < 1:
                                                        percentage = input(
                                                            "Enter the percentage return you wish to trade at: ")
                                                        trading_percentage_validation = project_functions.percentage_return_input_test(
                                                            percentage)
                                                        if trading_percentage_validation == "invalid entry":
                                                            print("you have made an invalid entry"'\n'
                                                                  "kindly note that the acceptable percentage is between 30-90 percent"'\n'
                                                                  "also any other character apart from digits or decimal input is not acceptable")
                                                        else:
                                                            print("Options saved")

                                    break_loop1 += 'B'
                                    break_loop2 += 'B'
                                    break_loop3 += 'B'
                                    break
                            else:
                                print("Incorrect password!")
                            break
                elif options == 'B':
                    Member_registration.member_registration()
                    break_loop1 += 'B'
                    break
                elif options not in ('A', 'B', 'Q'):
                    print("Selected option not valid!")
                else:
                    break_loop1 += 'B'
                    break
        else:
            if password in [username_key_match[i][0] for i in range(len(username_key_match))]:
                print("Login successful!")
                while True:
                    balance = project_functions.username_balance_check(username)
                    print(f"Welcome {username}!"'\n'
                          f"Your wallet balance is ${balance}"'\n'
                          f'Here are the current exchange rates of bitcoin :')
                    usd_rate = api_call('usd')
                    eth_rate = api_call('eth')
                    eur_rate = api_call('eur')
                    print(f'Exchange rate of USD to 1 BTC is {usd_rate}')
                    print(f'Exchange rate of ETH to 1 BTC is {eth_rate}')
                    print(f'Exchange rate of EURO to 1 BTC is {eur_rate}')
                    homepage_options = input("What will you like to do?"'\n'
                                             "A       Trade"'\n'
                                             "B       Deposit"'\n'
                                             "C       Check wallet balance"'\n'
                                             "Q       Logout"'\n'
                                             "Select an option: ").upper()
                    if homepage_options == 'B':
                        while True:
                            deposit_amount = input("Enter the amount you wish to deposit: ").strip()
                            if deposit_amount == "":
                                print("you have not made any valid entry")
                            amount_validation = project_functions.amount_validation(deposit_amount)
                            if amount_validation == ["invalid entry"]:
                                print("you have made an invalid entry"'\n'
                                      "Please note that special characters,letters, combination of both special characters and letters"'\n'
                                      "or the combination any of the previously mentioned with number is not an acceptable input"'\n')
                            else:
                                u_deposit_amount = project_functions.first_deposit_amount_check(deposit_amount)
                                user_id = project_functions.username_uid_recall(username)
                                userid_t = project_functions.userid_trans()
                                if u_deposit_amount == ["not below 200"] and [user_id] not in userid_t:
                                    print(f"Deposit of ${deposit_amount} successful!")
                                    project_functions.username_walletbalance_update(username, deposit_amount)
                                    today = datetime.datetime.now(tz=pytz.timezone('Africa/Lagos'))
                                    time_now = today.time().strftime('%H:%M:%S')
                                    date_now = today.date()
                                    cursor.execute(
                                        "INSERT INTO transaction_history(user_id, transaction_type, amount, transaction_date, transaction_time) "
                                        "VALUES (?,?,?,?,?)", (user_id, 'deposit', deposit_amount, date_now, time_now))
                                    conn.commit()
                                    break
                                elif u_deposit_amount == ["not below 200"] and user_id in userid_t:
                                    print(f"Deposit of ${deposit_amount} successful!")
                                    project_functions.username_walletbalance_update(username, deposit_amount)
                                    today = datetime.datetime.now(tz=pytz.timezone('Africa/Lagos'))
                                    time_now = today.time().strftime('%H:%M:%S')
                                    date_now = today.date()
                                    cursor.execute(
                                        "INSERT INTO transaction_history(user_id, transaction_type, amount, transaction_date, transaction_time) "
                                        "VALUES (?,?,?,?,?)", (user_id, 'deposit', deposit_amount, date_now, time_now))
                                    conn.commit()
                                    break
                                elif u_deposit_amount != ["not below 200"] and user_id in userid_t:
                                    print(f"Deposit of ${deposit_amount} successful!")
                                    project_functions.username_walletbalance_update(username, deposit_amount)
                                    today = datetime.datetime.now(tz=pytz.timezone('Africa/Lagos'))
                                    time_now = today.time().strftime('%H:%M:%S')
                                    date_now = today.date()
                                    cursor.execute(
                                        "INSERT INTO transaction_history(user_id, transaction_type, amount, transaction_date, transaction_time) "
                                        "VALUES (?,?,?,?,?)", (user_id, 'deposit', deposit_amount, date_now, time_now))
                                    conn.commit()
                                    break
                                else:
                                    print("Your first ever deposit can not be less than $200!")
            else:
                print("Incorrect password!")

mem_login()

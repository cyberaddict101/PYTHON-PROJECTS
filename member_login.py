import  datetime
import time
import pytz
import requests
import sqlite3
import Member_registration
import project_functions

project_functions.trans_hist_table()
project_functions.trading_hist_table()


conn = sqlite3.connect('CryptoTrading.db')
cursor = conn.cursor()



def api_call(coin):
	response = requests.get('https://api.coingecko.com/api/v3/exchange_rates')
	rates_json = response.json()
	return rates_json['rates'][coin]['value']


def mem_login():
	username = ''
	deposit_amount = ''
	trade_duration=''
	option_chosen = ''
	trade_amount=''
	trade_option =''
	username_email=''
	# accepting and validating username/email to login
	found = False
	while not found:
		username_email= input('Enter your username or email: ').lower().strip()
		if '@' in username_email:
			email_list = project_functions.email_recall()
			if username_email not in email_list:
				print(f'The email \'{username_email}\' is not associated with any account!')
				continue
			else:
				username = project_functions.email_username(username_email)
				found = True
		elif '@' not in username_email:
			username_list = project_functions.username_recall()
			if username_email in username_list:
				username = username_email
				found = True
			elif username_email =='':
				print('Empty string is not a valid input')
			else:
				print(f'Username \'{username_email}\' is not associated with any account!')
				continue

	# accepting and validating password
	key_match = False
	while not key_match:
		password = input('Enter password: ').strip().lower()
		encoded_password = project_functions.encode_password(password)
		key_recall = project_functions.username_key_recall(username)
		if encoded_password == key_recall:
			print('Login Successful!')
			key_match = True
		else:
			print('Incorrect password!')
			continue
	jump_out_of_homepage_loop =False
	while not jump_out_of_homepage_loop:
		balance = project_functions.username_balance_check(username)
		print(f"Welcome {username}!"'\n'
			  f"Your wallet balance is ${balance}"'\n'
			  f'Here are the current exchange rates of bitcoin :')
		usd_rate = api_call('usd')
		eth_rate = api_call('eth')
		eur_rate = api_call('eur')
		print(f'Exchange rate of USD to 1 BTC is {usd_rate}\nExchange rate of ETH to 1 BTC is {eth_rate}\nExchange rate of EURO to 1 BTC is {eur_rate}')
		homepage_options = input("What will you like to do?\nA.\tTrade\nB.\tDeposit\nC.\tCheck wallet balance\nQ.\tLogout\nSelect an option: ").upper()
		if homepage_options == 'B':
			jump_out_of_deposit_loop = False
			while not jump_out_of_deposit_loop:
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
						start_time = today.time().strftime('%H:%M:%S')
						date_now = today.date()
						cursor.execute(
							"INSERT INTO transaction_history(user_id, transaction_type, amount, transaction_date, transaction_time) "
							"VALUES (?,?,?,?,?)", (user_id, 'deposit', deposit_amount, date_now, start_time))
						conn.commit()
						jump_out_of_deposit_loop = True
					elif u_deposit_amount == ["not below 200"] and user_id in userid_t:
						print(f"Deposit of ${deposit_amount} successful!")
						project_functions.username_walletbalance_update(username, deposit_amount)
						today = datetime.datetime.now(tz=pytz.timezone('Africa/Lagos'))
						start_time = today.time().strftime('%H:%M:%S')
						date_now = today.date()
						cursor.execute(
							"INSERT INTO transaction_history(user_id, transaction_type, amount, transaction_date, transaction_time) "
							"VALUES (?,?,?,?,?)", (user_id, 'deposit', deposit_amount, date_now, start_time))
						conn.commit()
						jump_out_of_deposit_loop = True
					elif u_deposit_amount != ["not below 200"] and user_id in userid_t:
						print(f"Deposit of ${deposit_amount} successful!")
						project_functions.username_walletbalance_update(username, deposit_amount)
						today = datetime.datetime.now(tz=pytz.timezone('Africa/Lagos'))
						start_time = today.time().strftime('%H:%M:%S')
						date_now = today.date()
						cursor.execute(
							"INSERT INTO transaction_history(user_id, transaction_type, amount, transaction_date, transaction_time) "
							"VALUES (?,?,?,?,?)", (user_id, 'deposit', deposit_amount, date_now, start_time))
						conn.commit()
						jump_out_of_deposit_loop = True
					else:
						print("Your first ever deposit can not be less than $200!")
		elif homepage_options == 'A':
			jump_out_of_trade_loop = False
			while not jump_out_of_trade_loop:
				trade_pair = input("A\tEURO/BTC\nB\tUSD/BTC\nC\tETH/BTC\nSelect an option from the above: ").strip().upper()
				trade_pair_validation = project_functions.trade_pair_validation(trade_pair)
				if trade_pair_validation == 'INVALID INPUT':
					print('You have made an invalid input! Kindly input between A-C')
				else:
					if trade_pair == 'A':
						trade_pair = "EURO/BTC"
						pair_call = 'eur'
						pair = "EURO"
					elif trade_pair == "B":
						trade_pair = "USD/BTC"
						pair = "USD"
						pair_call = 'usd'
					else:
						trade_pair = "ETH/BTC"
						pair = "ETH"
						pair_call = 'eth'
						jump_out_of_trade_loop = True
					jump_out_of_option_direction_loop = False
					while not jump_out_of_option_direction_loop:
						option_direction = input(f"A.\tBTC will rise against {pair}\nB.\tBTC will drop against {pair}\nSelect an option above for your prediction: ").strip().upper()
						option_direction_validation = project_functions.trade_direction_validation(option_direction)
						if option_direction_validation == 'INVALID OPTION':
							print('You have made an invalid input! Kindly input between A-B')
						else:
							if option_direction == "A":
								direction = "rise"
								trade_option = direction
								option_direction = f"BTC to rise against {pair}"
								option_chosen = option_direction
							else:
								direction = "fall"
								trade_option = direction
								option_direction = f"BTC to fall against {pair}"
								option_chosen = option_direction
							jump_out_of_option_direction_loop = True
					jump_out_of_amount_to_trade_loop = False
					while not jump_out_of_amount_to_trade_loop:
						amount = input('How much will you like to trade?: ').strip()
						trading_amount_validation = project_functions.amount_validation(amount)
						if trading_amount_validation == ["invalid entry"]:
							print("you have made an invalid entry"'\n'
								  "Please note that special characters,letters, combination of both special characters and letters"'\n'
								  "or the combination any of the previously mentioned with number is not an acceptable input"'\n')
						else:
							balance = project_functions.username_balance_check(username)
							if int(amount) > balance:
								print("you can not stake/trade more than your wallet balance")
							else:
								trade_amount = amount
								jump_out_of_amount_to_trade_loop = True
					jump_out_of_trade_duration_loop = False
					while not jump_out_of_trade_duration_loop:
						duration = input("Enter tade time in minutes (between 1-3): ")
						duration_validation = project_functions.trade_duration_match(duration)
						if duration_validation == 'INVALID INPUT':
							print('You have made an invalid input!\ninput should be between 1-3 in minutes not seconds!)')
						else:
							trade_duration = (int(duration)*60)
							jump_out_of_trade_duration_loop = True
					jump_out_of_percentage_loop = False
					while not jump_out_of_percentage_loop:
						trade_percent = input("Enter the percentage return you wish to trade at: ")
						trading_percentage_validation = project_functions.percentage_return_input_test(trade_percent)
						if trading_percentage_validation == "invalid entry":
							print("you have made an invalid entry"'\n'
								  "kindly note that the acceptable percentage is between 30 - less than 100 percent"'\n'
								  "also any other character apart from digits or decimal input is not acceptable")
						else:
							user_id = project_functions.username_uid_recall(username)
							actual_stake_value = float(trade_amount)*0.01*float(trade_percent)
							wallet_balance = balance - actual_stake_value
							project_functions.trade_wallet_balance_update(wallet_balance, user_id)
							print(f"{trade_pair} trade placed successfully for "+option_chosen)
							print(f'Your wallet balance is {wallet_balance}')
							today = datetime.datetime.now(tz=pytz.timezone('Africa/Lagos'))
							start_time = time.n
							date_now = today.date()
							start_price = api_call(pair_call)
							for i in range(trade_duration):
								print((trade_duration - i))
								time.sleep(1)
							# sleep(trade_duration)
							end_price = api_call(pair_call)
							end_time = today.time().strftime('%H:%M:%S')
							if end_price > start_price and trade_option == "rise":
								trade_result = "WON"
								result_amount = f"+{actual_stake_value}"
								increment = wallet_balance + (2*actual_stake_value)
								project_functions.insert_trade_details(user_id, trade_pair, trade_option,trade_percent, trade_amount, date_now,
																				start_time,start_price, end_price, end_time,trade_result, result_amount)
								project_functions.trade_wallet_balance_update(increment,user_id)
								print(f"Trade complete you WON the trade your new account balance is {increment}")
								jump_out_of_percentage_loop = True
								jump_out_of_trade_loop = True
							else:
								trade_result = "LOSS"
								result_amount = f"-{actual_stake_value}"
								project_functions.insert_trade_details(user_id, trade_pair, trade_option, trade_percent,trade_amount, date_now,
																	   start_time, start_price, end_price, end_time,trade_result, result_amount)
								print(f"Trade complete you LOST the trade your account balance is {wallet_balance}")
								jump_out_of_percentage_loop = True
								jump_out_of_trade_loop = True

	print('remaining body of function')


mem_login()

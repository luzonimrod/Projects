##############################################################################
# server.py
##############################################################################
import random
import socket
from random import randrange

import chatlib
import select
import test

# GLOBALS
users = {}
questions = {}
logged_users = {} # a dictionary of client hostnames to usernames - will be used later
questions_asked = {}
messages_to_send = [] #list that contain tuple, client name and the message
ERROR_MSG = "Error! "
SERVER_PORT = 5678
SERVER_IP = '0.0.0.0'
questions_from_json =  test.load_questions_from_web()


# HELPER SOCKET METHODS
def build_and_send_message(conn, code, data):
	global messages_to_send

	full_msg = chatlib.build_message(code, data)
	messages_to_send.append(tuple((conn.getpeername(), full_msg)))
	add = conn.getsockname()
	print("[SERVER] " + str(add) + "  msg: " + full_msg)
	conn.send(full_msg.encode())

def print_client_sockets(conn):
	global logged_users
	for i,j in logged_users.items():
		print(i)
		print(j)


def recv_message_and_parse(conn):
	"""
    Recieves a new message from given socket,
    then parses the message using chatlib.
    Paramaters: conn (socket object)
    Returns: cmd (str) and data (str) of the received message.
    If error occured, will return None, None
    """
	full_msg = conn.recv(1024).decode()
	if(full_msg == ""):
		exit()
	add = conn.getsockname()
	print("[CLIENT]  "+ str(add) +" msg: " + full_msg)
	msg_code, msg = chatlib.parse_message(full_msg)

	return msg_code, msg

# Data Loaders #

def load_questions():
	"""
	Loads questions bank from file	## FILE SUPPORT TO BE ADDED LATER
	Recieves: -
	Returns: questions dictionary
	"""

	questions = {
				2313 : {"question":"How much is 2+2","answers":["3","4","2","1"],"correct":2},
				4122 : {"question":"What is the capital of France?","answers":["Lion","Marseille","Paris","Montpellier"],"correct":3}
				}

	return questions
def create_random_question(username):
	count = 0
	count2 = 0
	global questions_asked
	list1 = []
	quests = questions_from_json
	random_number = random.randint(1,9)
	new_question = ''
	if(type(users[username]['questions_asked']) != list):
		users[username]['questions_asked'] = list1
	for i,j in quests.items():
		if count == random_number:
			if(str(i) not in users[username]['questions_asked']):
				users[username]['questions_asked'].append(str(i))

				new_question = str(i) + '#'
				new_question += quests[i]['question'] + '#'
			elif(count == 10):
				return None

			for k in quests[i]['answers']:
				count2 +=1
				if count2 == 4:
					new_question += k
				else:
					new_question += k +'#'

		count += 1
	return new_question
def handle_question_message(conn,username):
	new_question = create_random_question(username)
	if new_question == None:
		build_and_send_message(conn, 'YOUR_QUESTION', "No more Questions")
	else:
		build_and_send_message(conn, 'YOUR_QUESTION', new_question)


def load_user_database():
	"""
	Loads users list from file	## FILE SUPPORT TO BE ADDED LATER
	Recieves: -
	Returns: user dictionary
	"""
	users = {}
	new_file = open("/Users/luzonimrod/Documents/Python/Users.txt",'r')
	for line in new_file:
		key, value = line.split()
		li = value.split(",")

		for i in range(len(li)):
			j = li[i].split(":")
			if i > 0:
				users[key].update({j[0]:j[1]})
			else:
				users[key] = {j[0]: j[1]}


	#users = {
	#		"test"		:	{"password":"test","score":0,"questions_asked":[]},
	#		"yossi"		:	{"password":"123","score":50,"questions_asked":[]},
	#		"master"	:	{"password":"master","score":200,"questions_asked":[]}
	#		}
	return users

	
# SOCKET CREATOR
def setup_socket():

	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.bind((SERVER_IP, SERVER_PORT))
	sock.listen()
	print("Listening on port " + str(SERVER_PORT))


	
	return sock

		
def send_error(conn, error_msg):
	"""
	Send error message with given message
	Recieves: socket, message error string from called function
	Returns: None
	"""
	# Implement code ...
	

def handle_answer_message(conn,username,answer):
	new_list = answer.split('#')
	quests = questions_from_json
	for i,j in quests.items():
		if i == int(new_list[0]):
			if j['correct'] ==  (new_list[1]):
				result = users[username]['score']
				result = int(result) + 5
				users[username]['score'] = str(result)
				build_and_send_message(conn,'CORRECT_ANSWER','')
			else:
				build_and_send_message(conn,'WRONG_ANSWER',j['correct'])




	
##### MESSAGE HANDLING
def handle_highscore_message(conn):
	global users
	uname_scores = ""
	for i,j in users.items():
		uname_scores += str(i) +':' + str(users[i]['score']) + '\n'


	build_and_send_message(conn, 'ALL_SCORE', uname_scores)

def handle_getscore_message(conn, username):
	global users
	current_username = username[conn.getpeername()]
	score = users[current_username]['score']
	build_and_send_message(conn,'YOUR_SCORE',str(score))
	# Implement this in later chapters

def handle_logged_message(conn):
	global logged_users
	new_str = ""
	count = 0
	counter = len(logged_users.values())
	for i,j in logged_users.items():
		count += 1
		if(counter == count):
			new_str += str(j)
		else:
			new_str += str(j) + ", "

	build_and_send_message(conn, "LOGGED_ANSWER", new_str)
	
def handle_logout_message(conn):
	"""
	Closes the given socket (in laster chapters, also remove user from logged_users dictionary)
	Recieves: socket
	Returns: None
	"""
	global logged_users
	print(logged_users)
	del logged_users[(conn.getpeername())]
	print(logged_users)
	build_and_send_message(conn,'LOGOUT','')
	# Implement code ...


def handle_login_message(conn, data):
	"""
	Gets socket and message data of login message. Checks  user and pass exists and match.
	If not - sends error and finished. If all ok, sends OK message and adds user and address to logged_users
	Recieves: socket, message code and data
	Returns: None (sends answer to client)
	"""
	global users  # This is needed to access the same users dictionary from all functions
	global logged_users	 # To be used later
	client_sockets = []
	#client_host, client_address = conn.accept()
	client_host = data
	#one,two = recv_message_and_parse(conn)
	new_list = data.split("#")

	if(new_list[0] in users.keys()):
		if (new_list[1] == users[new_list[0]]['password']):
			logged_users.update({conn.getpeername():new_list[0]})
			build_and_send_message(conn,"LOGIN_OK","")
		else:
			build_and_send_message(conn,"ERROR","Error! Password does not match!")
	else:
		build_and_send_message(conn,"ERROR","Error! Username does not exist")

	# Implement code ...


def handle_client_message(conn, cmd, data):
	"""
	Gets message code and data and calls the right function to handle command
	Recieves: socket, message code and data
	Returns: None
	"""
	if cmd == 'LOGIN':
		handle_login_message(conn,data)
	if cmd == 'MY_SCORE':
		handle_getscore_message(conn,logged_users)
	if cmd == 'HIGHSCORE':
		handle_highscore_message(conn)
	if cmd == 'LOGGED':
		handle_logged_message(conn)
	if cmd == 'LOGOUT':
		handle_logout_message(conn)
	if cmd == 'GET_QUESTION':
		handle_question_message(conn,logged_users[conn.getpeername()])
	if cmd == 'SEND_ANSWER':
		handle_answer_message(conn,logged_users[conn.getpeername()],data)

	#global logged_users	 # To be used later

	


def main():
	# Initializes global users and questions dicionaries using load functions, will be used later
	global users, client_socket
	global questions
	users = load_user_database()
	client_sockets = []
	print("Welcome to Trivia Server!")
	server_socket = setup_socket()
	#client_host, client_address = client_server.accept()
	#print("New Client Joined!", client_host.getsockname())
	while True:
		ready_to_read, ready_to_write, in_error = select.select([server_socket] + client_sockets, client_sockets, [])
		for current_socket in ready_to_read:
			if current_socket is server_socket:
				(client_socket, client_address) = current_socket.accept()
				print("New client joined!", client_address)
				client_sockets.append(client_socket)
			else:
				cmd, data = recv_message_and_parse(current_socket)
				if cmd == "LOGOUT":
					print("Connection closed", )
					client_sockets.remove(current_socket)
					handle_client_message(current_socket, cmd, data)
				else:
					handle_client_message(current_socket,cmd,data)
					messages_to_send.append((current_socket, data))
		for message in messages_to_send:
			current_socket, data = message
			if current_socket in ready_to_write:
				#current_socket.send(data.encode())
				messages_to_send.remove(message)


if __name__ == '__main__':
	main()

	
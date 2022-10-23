# Protocol Constants

CMD_FIELD_LENGTH = 16	# Exact length of cmd field (in bytes)
LENGTH_FIELD_LENGTH = 4   # Exact length of length field (in bytes)
MAX_DATA_LENGTH = 10**LENGTH_FIELD_LENGTH-1  # Max size of data field according to protocol
MSG_HEADER_LENGTH = CMD_FIELD_LENGTH + 1 + LENGTH_FIELD_LENGTH + 1  # Exact size of header (CMD+LENGTH fields)
MAX_MSG_LENGTH = MSG_HEADER_LENGTH + MAX_DATA_LENGTH  # Max size of total message
DELIMITER = "|"  # Delimiter character in protocol
DATA_DELIMITER = "#"  # Delimiter in the data part of the message

# Protocol Messages 
# In this dictionary we will have all the client and server command names

PROTOCOL_CLIENT = {
"login_msg" : "LOGIN",
"logout_msg" : "LOGOUT"
} # .. Add more commands if needed


PROTOCOL_SERVER = {
"login_ok_msg" : "LOGIN_OK",
"login_failed_msg" : "ERROR"
} # ..  Add more commands if needed


# Other constants

ERROR_RETURN = None  # What is returned in case of an error


def build_message(cmd, data):
	"""
	Gets command name (str) and data field (str) and creates a valid protocol message
	Returns: str, or None if error occured
	"""
	full_msg=""
	if cmd == 'LOGIN' or cmd == 'LOGOUT' or cmd == 'MY_SCORE' or cmd == 'HIGHSCORE' or cmd == 'GET_QUESTION'\
			or cmd == 'SEND_ANSWER' or cmd == 'LOGGED' or cmd == 'LOGIN_OK' or cmd == 'ERROR' \
			or cmd == 'YOUR_SCORE' or cmd == 'ALL_SCORE' or cmd == 'LOGGED_ANSWER' or cmd == 'YOUR_QUESTION'\
			or cmd == 'YOUR_ANSWER' or cmd == 'CORRECT_ANSWER' or cmd =='WRONG_ANSWER':
		size = len(data)
		full_msg += cmd + (" "*(16-len(cmd)))
		if (size <= 9 ):
			size = "|000" + str(size)+"|"
		elif(size > 9 and size <= 99):
			size = "|00" + str(size)+"|"
		elif (size > 99 and size <= 999):
			size = "|0" + str(size)+"|"
		full_msg += size + data
	else:
		return None

	return (full_msg)


def parse_message(data):
	count = 0
	num2 = 0
	num4 =""
	if not data:
		return (None,None)
	new_list = data.split("|")
	if len(new_list) != 3 :
		return (None,None)
	cmd = new_list[0].replace(" ", "")
	num = new_list[1]
	if (cmd == 'ALL_SCORE'):
		msg = new_list[-1]
		return cmd, msg
	if (cmd == 'YOUR_QUESTION' or cmd == 'WRONG_ANSWER' or cmd == 'CORRECT_ANSWER' or cmd == 'LOGGED_ANSWER'):
		msg = new_list[-1]
		return cmd,msg
	if (cmd == 'ERROR'):
		msg = new_list[-1]
		return cmd, msg
	for i in num:
		if(i.isdigit()):
			count += 1
			num2 = int(i)
			if(count == 3 or count == 4 and num2 > 0):
				num4 += i
				num2 = int(num4)
	if(num2 != len(new_list[-1])):
		return None,None
	if(count == 0):
		return None,None
	if(int(num) < 0 ):
		return None,None
	if(cmd == 'YOUR_SCORE'):
		msg = new_list[-1]
		return cmd,msg
	if (cmd == 'LOGOUT'):
		msg = new_list[-1]
		return cmd, msg
	if(new_list[-1].isnumeric() == False):
		msg = new_list[-1]
	else:
		cmd = None
		msg = None

	return (cmd,msg)

	
def split_data(msg, expected_fields):
	count = 0
	for i in msg:
		if i == '#':
			count += 1
	if count == expected_fields:
		new_list=msg.split("#")
	else:
		print(None)
		return
	return (new_list)

def join_data(msg_fields):
	"""
	Helper method. Gets a list, joins all of it's fields to one string divided by the data delimiter.
	Returns: string that looks like cell1#cell2#cell3
	"""
	new_string = ""
	count=len(msg_fields)
	for i in range(len(msg_fields)):
		if(i != count - 1):
			new_string += msg_fields[i] + "#"
		else:
			new_string += msg_fields[i]
	return (new_string)






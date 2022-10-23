import socket
import chatlib
import requests
import requests

SERVER_IP = "127.0.0.1"  # Our server will run on same computer as client
SERVER_PORT = 5678

# HELPER SOCKET METHODS
def build_send_recv_parse(conn,cmd,msg):

    data = chatlib.build_message(cmd, msg)
    #print(data)
    conn.send(data.encode())
    full_msg = conn.recv(1024).decode()
    msg_code, data = chatlib.parse_message(full_msg)
    if msg_code == 'ERROR':
        error_and_exit(data)



    #print(msg_code,data)

    return msg_code, data
def build_and_send_message(conn, code, data):
    """
    Builds a new message using chatlib, wanted code and message.
    Prints debug info, then sends it to the given socket.
    Paramaters: conn (socket object), code (str), data (str)
    Returns: Nothing
    """
    # Implement Code

    msg = chatlib.build_message(code,data)
    print(msg)
    conn.send(msg.encode())

def recv_message_and_parse(conn):
    """
    Recieves a new message from given socket,
    then parses the message using chatlib.
    Paramaters: conn (socket object)
    Returns: cmd (str) and data (str) of the received message.
    If error occured, will return None, None
    """
    full_msg = conn.recv(1024).decode()
    print("Server say " + full_msg)
    msg_code, msg = chatlib.parse_message(full_msg)
    print("msg_code,msg")
    print(msg_code,msg)
    return msg_code, msg

def get_score(conn):

    var1,var2 = build_send_recv_parse(conn,"MY_SCORE","")
    print(var1,var2)
def get_highscore(conn):

    var1, var2 = build_send_recv_parse(conn, "HIGHSCORE", "")
    print("High-Score table:")
    print(var2)
def play_question(conn):
    new_list = []
    count = 0
    answer_id = 0
    var1,var2 = build_send_recv_parse(conn,"GET_QUESTION", "")
    if (var2 == "No more Questions"):
        print("No more Questions")
        return
    #var2 = (var2.replace("#"," "))
    new_list = var2.split("#")
    new_list2 = []
    for i in new_list:
        if i == new_list[0]:
            answer_id = i
        if i == new_list[1]:
            print('Q: ' + i )
        else:
            new_list2.append(i)
            print(str(count) + '.' + i)
            count += 1
    del new_list2[0]
    choice = input("Please choose an answer [1-4]: ")
    if(choice == '1'):
        choice = new_list2[0]
    if (choice == '2'):
        choice = new_list2[1]
    if (choice == '3'):
        choice = new_list2[2]
    if (choice == '4'):
        choice = new_list2[3]

    choice = answer_id + '#' + choice
    var3, var4 = build_send_recv_parse(conn, "SEND_ANSWER", choice)
    if var3 == 'CORRECT_ANSWER':
        print("YES!!!!")
    if var3 == 'WRONG_ANSWER':
        print("Nope, correct answer is " + var4)




def connect():

    client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    client_socket.connect((SERVER_IP, SERVER_PORT))

    return client_socket


def error_and_exit(error_msg):
    if error_msg == 'Error! Username does not exist':
        print(error_msg)
        exit()
    if error_msg == 'Error! Password does not match!':
        print(error_msg)
        exit()

def get_logged_users(conn):
    var3, var4 = build_send_recv_parse(conn, "LOGGED", "")

    print("Logged users:")
    print(var4)

def login(conn):
    username = input("Please enter username: ")
    password = input("Please enter password: ")
    uname_and_pwd = username + "#" + password
    build_send_recv_parse(conn, chatlib.PROTOCOL_CLIENT["login_msg"],uname_and_pwd)
    print("Logged In!")
    #build_and_send_message(conn, chatlib.PROTOCOL_CLIENT["login_msg"],uname_and_pwd)
    #recv_message_and_parse(conn)
    #logout(conn)
    # Implement code

    pass

def logout(conn):
    # Implement code
    cmd = "LOGOUT"
    data = ""
    build_and_send_message(conn,cmd,data)

    pass

def main():
    client_connection = connect()
    login(client_connection)
    while True:
        print("p        Play a trivia question")
        print("s        Get my score")
        print("h        Get high score")
        print("l        Get logged users")
        print("q        Quit")
        choice = input("Please enter your choice: ")
        if(choice == 'p'):
            play_question(client_connection)
        if(choice == 's'):
            get_score(client_connection)
        if(choice == 'h'):
            get_highscore(client_connection)
        if (choice == 'l'):
            get_logged_users(client_connection)
        if(choice == 'q'):
            logout(client_connection)
            break
    #recv_message_and_parse(client_connection)



if __name__ == '__main__':
    main()

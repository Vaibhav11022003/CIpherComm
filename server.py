import socket
import threading
import hashlib
import sqlite3
import time 
import os
import rsa 
import emoji
import tqdm

public_key,private_key=rsa.newkeys(1024)

PORT=5050
IP=socket.gethostbyname(socket.gethostname())
ADDR=(IP,PORT)
FORMAT='utf-8'
HEADER=2048

DISCONNECT_MESSAGE='!DISCONNECT'
SEND_FILE='!SENDF'
REQUEST_FILE='!REQF'
NOT_CLIENT='!NOTCLIENT'
SERVER_FOLDER='E:/tkinter/project/'
LAST_FILE='<LAST>'
FILE_LIST='!FILELIST'

active_clients=[]
server_lock=threading.Lock()

server=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.bind(ADDR)

def handle_request_file_list(conn,addr):
    userdb=sqlite3.connect('userdata.db')
    cur=userdb.cursor()
    cur.execute("SELECT filename from files")
    for i in cur.fetchall():
        conn.sendall(i[0].encode(FORMAT))
        time.sleep(0.1)
    conn.sendall(LAST_FILE.encode(FORMAT))

def handle_send_file(conn,addr):
    file_name=conn.recv(HEADER).decode(FORMAT)
    file_size=int(conn.recv(HEADER).decode(FORMAT))
    index=file_name.find('.')
    new_name=file_name[:index]+'_copy'+file_name[index:]
    server_lock.acquire()
    userdb=sqlite3.connect('userdata.db')
    cur=userdb.cursor()
    cur.execute("INSERT OR IGNORE INTO files (filename) VALUES (?)",(new_name,))  
    userdb.commit()
    server_lock.release()
    new_name=os.path.join(SERVER_FOLDER,new_name)
    file=open(new_name,'wb')
    file_data=b""
    done=False
    progress=tqdm.tqdm(unit='B',unit_scale=True,unit_divisor=1000,total=file_size)
    while not done:
        if file_data[-5:]==b'<END>' :
            done=True
            break
        data=conn.recv(1024)
        file_data+=data
        progress.update(1024)
    if file_data[-5:]==b'<END>':
        file_data=file_data[:-5]
    print(f'{new_name} received...')
    file.write(file_data)
    file.close()

def handle_request_file(conn,addr):
    file_name=conn.recv(HEADER).decode(FORMAT)
    print(file_name)
    if not os.path.exists(file_name):
        conn.sendall(str(-1).encode(FORMAT))
        print(f'"{file_name}" not exist... ')
        return
    print(f'"{file_name}" sent at {addr}... ')
    file=open(file_name,'rb')
    file_data=file.read()
    file_size=os.path.getsize(file_name)
    conn.sendall(str(file_size).encode(FORMAT))
    conn.sendall(file_data)
    conn.send(b'<END>')
    file.close()

def send_all_text(message,username):
    for client in active_clients:
        if client[0]==username:
            continue
        client[1].sendall(rsa.encrypt(message.encode(FORMAT),client[2]))

def handle_client_text(conn,addr,username,public_partner):
    while True:
        message=rsa.decrypt(conn.recv(HEADER),private_key).decode(FORMAT)
        if message==SEND_FILE:
            handle_send_file(conn,addr)
        elif message==REQUEST_FILE:
            handle_request_file(conn,addr)
        elif not message or message==DISCONNECT_MESSAGE:
            send_all_text(f'{username} -> [LEFT] {username} has left the room...',username)
            break
        else:
            message=f'{username} -> {message}'
            print(message)
            send_all_text(message,username)


def handle_client_login(conn,addr):
    userdb=sqlite3.connect('userdata.db')
    cur=userdb.cursor()
    while True:
        username=conn.recv(HEADER).decode(FORMAT)
        if username==DISCONNECT_MESSAGE:
            conn.close()
            return
        if username==FILE_LIST:
            handle_request_file_list(conn,addr)
            conn.close()
            return
        if username==NOT_CLIENT:
            handle_request_file(conn,addr)
            conn.close()
            return
        password=conn.recv(HEADER)
        if password==DISCONNECT_MESSAGE:
            conn.close()
            return
        password=hashlib.sha256(password).hexdigest()
        cur.execute('SELECT * from userdata where username = ? and password = ? and status = True',(username,password))
        if cur.fetchall():
            conn.sendall('LOGIN IS SUCCESSFUL...'.encode(FORMAT))
            break
        else :
            conn.sendall('LOGIN ATTEMPT FAILED...'.encode(FORMAT))
            time.sleep(3)
    
    public_partner=rsa.PublicKey.load_pkcs1(conn.recv(HEADER))
    conn.sendall(public_key.save_pkcs1('PEM'))


    server_lock.acquire()
    print(f'[JOINED] {username} with adress {addr} has joined the room...')
    active_clients.append((username,conn,public_partner))
    cur.execute('UPDATE userdata SET status = False where username=? and password=? and status = True',(username,password))
    userdb.commit()
    server_lock.release()

    handle_client_text(conn,addr,username,public_partner)

    server_lock.acquire()
    print(f'[LEFT] {username} with adress {addr} has left the room...')
    active_clients.remove((username,conn,public_partner))
    cur.execute("UPDATE userdata SET status=True where username=? and password=? and status=False",(username,password))
    userdb.commit()
    server_lock.release()
    conn.close()


def add_new_user(cur,conndb,username,password):
    password=hashlib.sha256(password.encode(FORMAT)).hexdigest()
    server_lock.acquire()
    cur.execute("INSERT INTO userdata (username,password,status) VALUES (?,?,?)",(username,password,True))
    conndb.commit()
    server_lock.release()

def change_username(cur,conndb,oldusername,newusername):
    server_lock.acquire()
    cur.execute("UPDATE userdata SET username=? where username=? and status=True",(newusername,oldusername))
    conndb.commit()
    server_lock.release()

def change_password(cur,conndb,username,password):
    password=hashlib.sha256(password.encode(FORMAT)).hexdigest()
    server_lock.acquire()
    cur.execute("UPDATE userdata SET password=? where username=? and status=True",(username,password))
    conndb.commit()
    server_lock.release()

def remove_user(cur,conndb,username,password):
    password=hashlib.sha256(password.encode(FORMAT)).hexdigest()
    server_lock.acquire()
    cur.execute("DELETE FROM userdata where username=? and password=? and status=True",(username,password))
    conndb.commit()
    server_lock.release()

def print_all_user(cur,conndb):
    cur.execute("SELECT * from userdata")
    for i in cur.fetchall():
        print(i)

def print_all_files(cur,conndb):
    cur.execute("SELECT filename from files")
    for i in cur.fetchall():
        print(i[0])

def server_end():
    conndb=sqlite3.connect('userdata.db')
    cur=conndb.cursor()
    flag="open"
    while flag!="close":
        flag=input()
        if flag=="remove_user":
            pass
            username=input("enter username:  ")
            password=input("enter password:  ")
            remove_user(cur,conndb,username,password)
        elif flag=="add_new_user":
            username=input("enter username:  ")
            password=input("enter password:  ")
            add_new_user(cur,conndb,username,password)
        elif flag=="change_username":
            oldusername=input("enter old-username:  ")
            newusername=input("enter new-username:  ")
            change_username(cur,conndb,oldusername,newusername)
        elif flag=="change_password":
            username=input("enter username:  ")
            password=input("enter password:  ")
            change_password(cur,conndb,username,password)
        elif flag=="print_all_user":   
            print_all_user(cur,conndb)
        elif flag=='print_all_files':
            print_all_files(cur,conndb)

    server_lock.acquire()
    cur.execute("UPDATE userdata SET status=True")
    conndb.commit()
    for client in active_clients:
        client[1].sendall(DISCONNECT_MESSAGE.encode(FORMAT))
        client[1].close()
    active_clients.clear()
    server_lock.release()
    os._exit(1)


def start():
    server.listen()
    print(f'[LISTENING] server is listening at {ADDR}...')
    while True:
        conn,addr=server.accept()
        thread=threading.Thread(target=handle_client_login,args=(conn,addr))
        thread.start()

thread=threading.Thread(target=server_end,args=())
thread.start()
start()



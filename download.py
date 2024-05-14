import socket
import threading
import os
import time
import hashlib
import rsa
import tqdm

#contants 
public_key,private_key=rsa.newkeys(1024)
public_partner=None
client_lock=threading.Lock()

PORT=5050
IP=socket.gethostbyname(socket.gethostname())
ADDR=(IP,PORT)
FORMAT='utf-8'
HEADER=2048
DISCONNECT_MESSAGE='!DISCONNECT'
SEND_FILE='!SENDF'
REQUEST_FILE='!REQF'
NOT_CLIENT='!NOTCLIENT'

def handle_request_file():
    file_name=input('enter file to request:')
    if file_name==DISCONNECT_MESSAGE:
        return True
    client.sendall(file_name.encode(FORMAT))
    file_size=int(client.recv(HEADER).decode(FORMAT))
    if file_size==-1:
        return False
    print(file_size)
    index=file_name.find('.')
    new_file_name=file_name[:index]+'_copy'+file_name[index:]
    file=open(new_file_name,'wb')
    file_data=b''
    done=False
    progress=tqdm.tqdm(unit='B',unit_scale=True,unit_divisor=1000,total=file_size)
    i=0
    while not done:
        print(i)
        if file_data[-5:]==b'<END>' :
            done=True
            break
        data=client.recv(1024)
        file_data+=data
        progress.update(1024)
        i=i+1
    if file_data[-5:]==b'<END>':
        print('yes')
        file_data=file_data[:-5]
    print('received file...')
    file.write(file_data)
    file.close()
    return True

client=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
try :
    client.connect(ADDR)
    client.sendall(NOT_CLIENT.encode())
    done=False
    while not done:
        done=handle_request_file()
    client.close()
    os._exit(1)
except:
    print("[SERVER INACTIVE] app will be closed shortly")
    time.sleep(3)
    os._exit(1)


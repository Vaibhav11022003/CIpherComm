import socket
import threading
import os
import time
import hashlib
import rsa
import tqdm
import subprocess

from tkinter import *
from ttkbootstrap import *
from ttkbootstrap import Style
from customtkinter import *
import emoji
from PIL import Image,ImageTk

#contants 
public_key,private_key=rsa.newkeys(1024)
public_partner=None

PORT=5050
IP=socket.gethostbyname(socket.gethostname())
ADDR=(IP,PORT)
FORMAT='utf-8'
HEADER=2048

DISCONNECT_MESSAGE='!DISCONNECT'
SEND_FILE='!SENDF'
REQUEST_FILE='!REQF'
NOT_LOGGED_IN=True
NOT_CLIENT='!NOTCLIENT'
LAST_FILE='<LAST>'
FILE_LIST='!FILELIST'

client=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
try :
    client.connect(ADDR)
except:
    print("[SERVER INACTIVE] app will be closed shortly")
    time.sleep(3)
    os._exit(1)

def handle_send_file():
    filename=filedialog.askopenfilename(initialdir='E:\tkinter',title='select a file',)
    index=filename.rindex('/')
    file_name=filename[index+1:]
    client.sendall(rsa.encrypt(SEND_FILE.encode(FORMAT),public_partner))
    your_text(f'["{file_name}" FILE UPLOADED]\n')
    print(f'["{file_name}" file uploaded...]')
    file=open(filename,'rb')
    file_data=file.read()
    file_size=os.path.getsize(filename)
    client.sendall(file_name.encode(FORMAT))
    time.sleep(1)
    client.sendall(str(file_size).encode(FORMAT))
    time.sleep(1)
    client.sendall(file_data)
    time.sleep(1)
    client.sendall(b'<END>')
    file.close()

def handle_request_file_sub(clientchild):
    file_name=entry_file_name_set.get()
    entry_file_name.update_idletasks()
    time.sleep(1)
    file_name=entry_file_name_set.get()
    clientchild.sendall(file_name.encode(FORMAT))
    file_size=int(clientchild.recv(HEADER).decode(FORMAT))
    if file_size==-1:
        print(f'["{file_name}" not exists...]')
        your_text(f'["{file_name}" not exists...]')
        return 
    print(file_size)
    index=file_name.find('.')
    new_file_name=file_name[:index]+'_copy'+file_name[index:]
    file=open(new_file_name,'wb')
    file_data=b''
    done=False
    progress=tqdm.tqdm(unit='B',unit_scale=True,unit_divisor=1000,total=file_size)
    while not done:
        if file_data[-5:]==b'<END>' :
            done=True
            break
        data=clientchild.recv(1024)
        file_data+=data
        progress.update(1024)
    if file_data[-5:]==b'<END>':
        print('yes')
        file_data=file_data[:-5]
    print(f'"{file_name}" received...')
    your_text(f'"{file_name}" received...')
    file.write(file_data)
    file.close()
    return
def handle_request_file():
    file_name=entry_file_name_set.get()
    entry_file_name.update_idletasks()
    time.sleep(0.1)
    file_name=entry_file_name_set.get()
    if not file_name or file_name=='ENTER FILE NAME WITH EXTENSION: ':
        entry_file_name_set.set('ENTER FILE NAME WITH EXTENSION: ')
        return
    clientchild=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    try :
        clientchild.connect(ADDR)
        clientchild.sendall(NOT_CLIENT.encode())
        done=False
        handle_request_file_sub(clientchild)
        clientchild.close()
        entry_file_name_set.set("FILE RECEIVE: ")
    except:
        print("[SERVER INACTIVE] app will be closed shortly")
        time.sleep(3)

def recv_text():
    while True:
        message=rsa.decrypt(client.recv(HEADER),private_key).decode(FORMAT)
        index=message.find('->')
        username=message[:index]+' :'
        message=message[index+3:]
        other_text(username,message).pack(fill='x',pady=6)
        canvas.update_idletasks()
        canvas.configure(scrollregion=canvas.bbox('all'))

def send_text():
    entry_username.focus_set()
    text_message.configure(state='normal')
    message=text_message.get(1.0,END)
    if message[:-1]=='ENTER MESSAGE : ':
        return
    text_message.delete(1.0,END)
    text_message.insert(INSERT,'ENTER MESSAGE : ')
    message=message[:len(message)-1]
    if message=='' or not message:
        return
    print(message)
    client.sendall(rsa.encrypt(message.encode(FORMAT),public_partner))
    your_text(message)
    if message==DISCONNECT_MESSAGE:
       client.close()
       os._exit(1)

def start():
    username=enter_username.get()
    password=enter_password.get()
    client.sendall(username.encode(FORMAT))
    client.sendall(password.encode(FORMAT))
    message=client.recv(HEADER).decode(FORMAT)
    if message=='LOGIN IS SUCCESSFUL...':
        label_status['text']=message+f"{  emoji.emojize(':beaming_face_with_smiling_eyes:')}"
    else :
        label_status['text']=message+f"{  emoji.emojize(':disappointed_face:')}"
    enter_username.set("")
    enter_password.set("")
    if message!='LOGIN IS SUCCESSFUL...':
        return
    global NOT_LOGGED_IN
    NOT_LOGGED_IN=False
    emoji_button_1.configure(state='normal')
    emoji_button_2.configure(state='normal')
    emoji_button_3.configure(state='normal')
    emoji_button_4.configure(state='normal')
    emoji_button_5.configure(state='normal')
    emoji_button_6.configure(state='normal')
    button_message.configure(state='normal')
    button_req_file.configure(state='normal')
    button_send_file.configure(state='normal')
    button_file_list.configure(state='normal')
    entry_file_name['state']='normal'
    enter_username.set(username)
    button_signin['state']='disabled'
    entry_username['state']='disabled'
    entry_password['state']='disabled'
    text_message.configure(state='normal')
    text_message.insert(INSERT,'ENTER MESSAGE : ')
    entry_file_name_set.set('ENTER FILE NAME WITH EXTENSION: ')
    client.sendall(public_key.save_pkcs1('PEM'))
    global public_partner
    public_partner=rsa.PublicKey.load_pkcs1(client.recv(HEADER))
    
    thread=threading.Thread(target=recv_text,args=())
    thread.start()


root = Window()
style = Style(theme='pulse')
root.geometry('900x800+1000+100')
root.resizable(False,False)
root.title('CIPHER COMM')
style.map('TButton',
          foreground=[('pressed', 'white'),
                      ('active', 'white')],
          background=[('pressed', '#007bff'),
                      ('active', '#0056b3'),
                      ('!disabled', '#007bff'),
                      ('disabled', '#ced4da')],
          font=[('!disabled', ('Helvetica', 12)),
                ('disabled', ('Helvetica', 12, 'italic'))],
          relief=[('pressed', 'sunken'),
                  ('!disabled', 'raised'),
                  ('disabled', 'flat')])

style.map('TEntry',
          font=[('!focus', ('Helvetica', 12)),
                ('focus', ('Helvetica', 12, 'bold'))],
          fieldbackground=[('focus', '#007bff'),
                           ('!focus', '#f8f9fa')],
          foreground=[('focus', 'white'),
                      ('!focus', 'black')],
          bordercolor=[('focus', '#007bff'),
                       ('!focus', '#ced4da')],
          borderwidth=[('focus', 1),
                       ('!focus', 1)])

style.configure('Vertical.TScrollbar',
                gripcount=0,
                background='#f8f9fa',
                troughcolor='#f8f9fa',
                bordercolor='#f8f9fa',
                arrowcolor='#495057',
                arrowrelief='flat',
                highlightcolor='#f8f9fa',
                lightcolor='#f8f9fa',
                darkcolor='black',  # Change the thumb color to black
                width=10,
                relief='flat')

style.map('Vertical.TScrollbar',
          background=[('active', '#007bff'),
                      ('!disabled', '#f8f9fa')],
          arrowcolor=[('active', '#f8f9fa'),
                      ('!disabled', '#f8f9fa')])

#upper frame part
logo=ImageTk.PhotoImage(Image.open('applogo.png').resize((150,150),Image.LANCZOS))
enter_username=StringVar()
enter_password=StringVar()
upper_frame=CTkFrame(root,fg_color='transparent',border_width=1)
upper_frame_1=Frame(upper_frame)
upper_frame_2=Frame(upper_frame)
label_logo=Label(upper_frame_2,image=logo )
# label_logo=Label(upper_frame_2,text='C',font='Calibri 80')
upper_frame_2_1=Frame(upper_frame_2)
label_app_name=Label(upper_frame_2_1,text='   CIPHER COMM   ',font='Calibri 16',borderwidth=3,relief='groove',justify='center')
label_made_by=Label(upper_frame_2_1,text='Made by:   ',font='Calibri 10')
label_vaibhav=Label(upper_frame_2_1,text='Vaibhav      ',font='Calibri 10')
label_khushi=Label(upper_frame_2_1,text='Khushi        ',font='Calibri 10')
label_username=Label(upper_frame_1,text='USERNAME : ',font='Calibri 12')
label_password=Label(upper_frame_1,text='PASSWORD : ',font='Calibri 12')
entry_username=Entry(upper_frame_1,textvariable=enter_username,style='TEntry')
entry_password=Entry(upper_frame_1,textvariable=enter_password,show='*',style='TEntry')
button_signin=Button(upper_frame_1,text='SIGN IN',command=start ,style='TButton')
label_status=Label(upper_frame_1,text='LOGIN STATUS: ',font='Calibri 12')

upper_frame.pack(fill='both',pady=1)
upper_frame_1.pack(side='left',padx=10)
upper_frame_2.pack(side='right',pady=2)
label_logo.pack(side='left',fill='both',padx=4)
upper_frame_2_1.pack(side='left',fill='both')
label_app_name.pack(ipady=3,padx=6,pady=6)
label_khushi.place(relx=1,rely=0.9,anchor='se')
label_vaibhav.place(relx=1,rely=0.7,anchor='se')
label_made_by.place(relx=1,rely=0.5,anchor='se')
upper_frame_1.columnconfigure((0,1,2),weight=1,uniform='a')
upper_frame_1.rowconfigure((0,1,2),weight=1,uniform='a')
label_username.grid(row=0,column=0,pady=4)
label_password.grid(row=1,column=0,pady=4)
button_signin.grid(row=2,column=0,pady=4)
entry_username.grid(row=0,column=1,columnspan=2,pady=4)
entry_password.grid(row=1,column=1,columnspan=2,pady=4)
label_status.grid(row=2,column=1,columnspan=2,pady=4)


#middle part

def your_text(message):
    text=message
    newtext=''
    index=0
    while index<len(text):
        newtext+=text[index:index+30]
        index+=30
        if index<len(text):
            newtext+='\n'
    frame=Frame(canvas_frame)
    label_username=Label(frame,text='<- YOU',font=('Calibri',14))
    label_text=Label(frame,text=newtext,font=('Calibri',14))
    frame.columnconfigure((0,1,2,3,4),weight=1,uniform='a')
    frame.rowconfigure(0,weight=1,uniform='a')
    label_username.grid(row=0,column=4,sticky='ne')
    label_text.grid(row=0,column=0,columnspan=4,sticky='ne')
    frame.pack(fill='both',pady=6)
    canvas.update_idletasks()
    canvas.configure(scrollregion=canvas.bbox('all'))

def other_text(username,message):
    text=message
    frame=Frame(canvas_frame)
    label_username=Label(frame,text=f'{username.upper()}-> ',font=('Calibri',12))
    label_text=Label(frame,text=text,font=('Calibri',12))
    frame.columnconfigure((0,1,2,3,4),weight=1,uniform='a')
    frame.rowconfigure(0,weight=1,uniform='a')
    label_username.grid(row=0,column=0,sticky='nw')
    label_text.grid(row=0,column=1,columnspan=4,sticky='nw')
    canvas.update_idletasks()
    canvas.configure(scrollregion=canvas.bbox('all'))
    return frame

def file_list():
    for widget in canvas_frame_2.winfo_children()[1:]:
        widget.destroy()
    client_file_list=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    client_file_list.connect(ADDR)
    client_file_list.sendall(FILE_LIST.encode(FORMAT))
    files=[]
    done=False
    while not done:
        filename=client_file_list.recv(HEADER).decode(FORMAT)
        if filename==LAST_FILE:
            done=True
        else:
            files.append(filename)
    client_file_list.close()
    files.sort()
    def create_button(i):
        def button_click():
            entry_file_name_set.set(i)

        button=Button(canvas_frame_2,text=i,command=button_click,style='Warning.TButton')
        button.pack(pady=4)
    for i in files:
        create_button(i)
    canvas_2.update_idletasks()
    canvas_2.configure(scrollregion=canvas_2.bbox('all'))

middle_frame=CTkFrame(root,border_width=1,fg_color='red')
middle_frame_1=CTkFrame(middle_frame)
middle_frame_2=CTkFrame(middle_frame)
canvas=Canvas(middle_frame_1,width=550)
canvas_2=Canvas(middle_frame_2,width=324)
scrollbar=Scrollbar(middle_frame_1,orient='vertical',command=canvas.yview,style='Vertical.TScrollbar')
scrollbar_2=Scrollbar(middle_frame_2,orient='vertical',command=canvas_2.yview,style='Vertical.TScrollbar')
canvas_frame=Frame(canvas)
label_chat_room=Label(canvas_frame,text='CHAT ROOM',font='Calibri 20')
canvas_frame_2=Frame(canvas_2)
button_file_list=Button(canvas_frame_2,text='GET FILE LIST',command=file_list,style='TButton',state='disabled')

middle_frame.pack(fill='both',expand=True)
middle_frame_1.pack(side='left',fill='y')
middle_frame_2.pack(side='right',fill='y')
button_file_list.pack(pady=10)
canvas.pack(side='left',fill='both')
canvas_2.pack(side='left',fill='both')
scrollbar.pack(side='right',fill='y')
scrollbar_2.pack(side='right',fill='y')
label_chat_room.pack()
canvas.configure(yscrollcommand=scrollbar.set)
canvas_2.configure(yscrollcommand=scrollbar_2.set)
canvas.create_window((0,0),window=canvas_frame,anchor='nw',width=540)
canvas_2.create_window((0,0),window=canvas_frame_2,anchor='nw',width=314)
canvas.bind('<Configure>',lambda event:canvas.configure(scrollregion=canvas.bbox('all')))
canvas_2.bind('<Configure>',lambda event:canvas_2.configure(scrollregion=canvas_2.bbox('all')))

# bottom frame part
emoji_list=[':angry_face:',':astonished_face:',':grinning_face_with_sweat:',':rolling_on_the_floor_laughing:',':crying_face:',':face_with_rolling_eyes:']

bottom_frame=CTkFrame(root,fg_color='transparent',border_width=1)
bottom_frame_1=Frame(bottom_frame)
text_message=Text(bottom_frame_1,width=40,height=7,font=('Calibri',12),state='disabled')

text_message.bind('<FocusIn>',lambda event :text_message.delete(1.0,END))
text_message.bind('<KeyPress>',lambda event:check_text_limit(event))
bottom_frame_1_1=Frame(bottom_frame_1,width=70)
button_message=Button(bottom_frame_1_1,text='SEND',
                         command=send_text,state='disabled',style='TButton')
frame_emojis=Frame(bottom_frame_1_1,width=70)

bottom_frame_2=Frame(bottom_frame)
entry_file_name_set=StringVar(value='ENTER FILE NAME WITH EXTENSION: ')
entry_file_name=Entry(bottom_frame_2,state='disabled',textvariable=entry_file_name_set,style='TEntry')
entry_file_name.bind('<FocusIn>',lambda event :entry_file_name.delete(0,END))
bottom_frame_2_1=Frame(bottom_frame_2)
button_req_file=Button(bottom_frame_2_1,text="DOWNLOAD\nFILE",command=handle_request_file,state='disabled',style='TButton')
button_send_file=Button(bottom_frame_2_1,text="UPLOAD\nFILE",command=handle_send_file,state='disabled',style='TButton')

bottom_frame.pack(side='bottom',fill='both')
bottom_frame_1.pack(side='left',fill='both',padx=10,pady=4)
bottom_frame_2.pack(side='right',fill='both',padx=10,pady=4)
entry_file_name.pack(fill='x',padx=6,pady=10)
bottom_frame_2_1.pack(fill='both',pady=10)
button_req_file.pack(side='left',expand=True,fill='both',pady=40,padx=6)
button_send_file.pack(side='left',expand=True,fill='both',pady=40,padx=6)
text_message.pack(side='left',fill='both',pady=8)
bottom_frame_1_1.pack(side='left',fill='both')
button_message.pack(pady=8,padx=4)
frame_emojis.pack(padx=4,pady=8)
frame_emojis.columnconfigure((0,1,2),weight=1,uniform='a')
frame_emojis.rowconfigure((0,1),weight=1,uniform='a')

def handle_emoji(em):
    text=text_message.get(1.0,END)
    if text[:-1]=='ENTER MESSAGE : ':
        text_message.delete(1.0,END)
    if len(text.encode(FORMAT))+len(emoji.demojize(em).encode(FORMAT))>=116:
        text_message.configure(state='disabled')
    else:
        text_message.insert(INSERT,f'{emoji.emojize(em)}')

def check_text_limit(event):
    text=text_message.get(1.0,END)
    if len(text.encode(FORMAT))>=116:
            text_message.delete(1.0,END)
            text_message.insert(INSERT,text[:-1])
            text_message.configure(state='disabled')

emoji_button_1=CTkButton(frame_emojis,text=f'{emoji.emojize(":angry_face:")}',
                           fg_color='transparent',font=('Calibri',24),width=1,text_color='black',state='disabled',
                           command=lambda:handle_emoji(":angry_face:"))
emoji_button_1.grid(row=0,column=0,sticky='nw')

emoji_button_2=CTkButton(frame_emojis,text=f'{emoji.emojize(":astonished_face:")}',
                           fg_color='transparent',font=('Calibri',24),width=1,text_color='black',state='disabled',
                           command=lambda:handle_emoji(":astonished_face:"))
emoji_button_2.grid(row=0,column=1,sticky='nw')

emoji_button_3=CTkButton(frame_emojis,text=f'{emoji.emojize(":grinning_face_with_sweat:")}',
                           fg_color='transparent',font=('Calibri',24),width=1,text_color='black',state='disabled',
                           command=lambda:handle_emoji(":grinning_face_with_sweat:"))
emoji_button_3.grid(row=0,column=2,sticky='nw')

emoji_button_4=CTkButton(frame_emojis,text=f'{emoji.emojize(":rolling_on_the_floor_laughing:")}',
                           fg_color='transparent',font=('Calibri',24),width=1,text_color='black',state='disabled',
                           command=lambda:handle_emoji(":rolling_on_the_floor_laughing:"))
emoji_button_4.grid(row=1,column=0,sticky='nw')

emoji_button_5=CTkButton(frame_emojis,text=f'{emoji.emojize(":crying_face:")}',
                           fg_color='transparent',font=('Calibri',24),width=1,text_color='black',state='disabled',
                           command=lambda:handle_emoji(":crying_face:"))
emoji_button_5.grid(row=1,column=1,sticky='nw')

emoji_button_6=CTkButton(frame_emojis,text=f'{emoji.emojize(":face_with_rolling_eyes:")}',
                           fg_color='transparent',font=('Calibri',24),width=1,text_color='black',state='disabled',
                           command=lambda:handle_emoji(":face_with_rolling_eyes:"))
emoji_button_6.grid(row=1,column=2,sticky='nw')

root.mainloop()
if NOT_LOGGED_IN:
    client.sendall(DISCONNECT_MESSAGE.encode(FORMAT))
else: 
    client.sendall(rsa.encrypt(DISCONNECT_MESSAGE.encode(FORMAT),public_partner))
client.close()
os._exit(1)

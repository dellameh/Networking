import re
import os
import time
import socket
import pyautogui
from PIL import ImageGrab

FORMAT="utf-8"

x=y=0

host = socket.gethostname()  
port = 5000 
client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

print('Waiting for connection response')
try:
    client_socket.connect((host, port))
except socket.error as e:
    print(str(e))
res = client_socket.recv(1024)



while True:

    data = client_socket.recv(1024).decode() 
    print('Received from server: ' + data)  
        
    # -----> take screenshot 
    if data == "1":
        ImageGrab.grab().save("sc.jpeg","JPEG")  
        sc=open("sc.jpeg","rb")
        scdata=sc.read(2048)
        client_socket.send("received_image.jpeg".encode())
        msg = client_socket.recv(1024).decode(FORMAT)
        print(f"[SERVER]: {msg}")
        sc_size=os.path.getsize("sc.jpeg")
        client_socket.send(str(sc_size).encode(FORMAT))
        msg = client_socket.recv(1024).decode(FORMAT)
        print(f"[SERVER]: {msg}")
        
        while scdata:
            client_socket.send(scdata)
            scdata=sc.read(2048)
        
        msg = client_socket.recv(1024).decode(FORMAT)
        print(f"[SERVER]: {msg}")
        
        sc.close()  
        client_socket.close() 
    
    
    # -----> move mouse 
    if data == f"2":
         client_socket.send("give x and y".encode())
         msg = client_socket.recv(1024).decode(FORMAT)
         print(msg)
         mokhtasat=list(map(int, re.findall(r'\d+', msg)))
         pyautogui.moveTo(mokhtasat[0], mokhtasat[1])
    
    
    # -----> send directory list 
    if data == "3":
        data=os.listdir()
        y = str(data)
        client_socket.send(y.encode())
        client_socket.send("list sent".encode())
        client_socket.recv(1024).decode()
        ack=client_socket.recv(1024).decode()
        #change directory or not?
        if ack== "ok":
            pass
        else:
            client_socket.send("send a file path".encode())
            path=client_socket.recv(1024).decode()
            os.chdir(path)
            data=os.listdir()
            y = str(data)
            client_socket.send(y.encode())
            client_socket.send("list sent".encode())
        
        # -----> transfer file 
        file_name=client_socket.recv(1024).decode(FORMAT)
        file=open(file_name,"r")
        transfer=file.read(1024)
        client_socket.send(transfer.encode(FORMAT))
        msg=client_socket.recv(1024).decode()
        print(msg)
        file.close()
    client_socket.close()

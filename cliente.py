# Importação de algumas bibliotecas
import socket
import threading
import time
import sys

# Definição das variáveis
host = "10.3.14.35"
port = 7777
buffer_size = 2048

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)   # Criação de um objeto socket
s.connect((host, port))                                 # Uso do connect para fazer a conexão com host e porta

nickname = input("Nickname: ")                          # TesteSonia


def receive():
    while True:
        try:
            mensagem = s.recv(buffer_size).decode()
            
            if mensagem != "":
                print(mensagem)
                
            time.sleep(0.2)
        except:
            print("Servidor desligado!")
            s.close()
            break


def write():
    while True:
        try:
            mensagem = input("")
    
            mensagem_bytes = nickname + ": " + mensagem
            s.send(mensagem_bytes.encode())
            time.sleep(0.2)
        except:
            s.close()
            sys.exit(0)


receive_thread = threading.Thread(name="receive", target=receive)
receive_thread.start()

write_thread = threading.Thread(name="write", target=write)
write_thread.start()

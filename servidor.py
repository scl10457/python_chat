# Importação de algumas bibliotecas
import socket
import threading
import time

# Definição das variáveis
host = "192.168.1.50"        # IP do servidor (PS: O IP do host tem que ser o IPv4 não pode ser 127.0.0.1 ou localhost)
port = 7777                  # Porta em que o servidor vai correr
buffer_size = 2048           # Tamanho dos caracteres

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)   # Criação de um objeto socket
s.bind((host, port))                                    # Uso do bind para fazer a conexão com host e porta
s.listen(5)

clientes = []       # Criação de uma lista onde vão ser colocados todos os clientes que se conectarem ao servidor


def broadcast(cliente, mensagem):   # Criação de uma função para envio das mensagens enviadas dos clientes para todos os clientes
    for c in clientes:              # Ciclo que vai percorrer todos os clientes na lista clientes[]
        if cliente != c:            # Envia a mensagem para todos os clientes conectados com a exepção do cliente que a enviou
            c.send(mensagem)
     
        
def handle(client, endereco):       # Função que vai controlar a ligação estabelecida pelos clientes
    while True:
        try:
            mensagem = client.recv(buffer_size)     # Vai receber os bytes enviados pelo cliente
            print(mensagem.decode())                # Mostra a mensagem convertida de bytes para string e apresenta-a no servidor
            broadcast(client, mensagem)             # Executa a função broadcast para enviar a mensagem para todos os clientes
            time.sleep(0.2)                         # Delay da thread
        except:
            erro = str(endereco) + " saiu!"         # Criação da mensagem quando o cliente sai
            print(erro)
            broadcast(client, erro.encode())        # Executa a função broadcast com a mensagem de saída do cliente
            clientes.remove(client)                 # Remove o cliente da lista clientes[]
            client.close()                          # Fecha a conexão do cliente
            break


def receber():                      # Função que vai receber as conexões dos clientes
    while True:
        cliente, endereco = s.accept()              # Criação de duas variáveis para a ligação
        clientes.append(cliente)                    # Adiciona o cliente à lista clientes[]
        print(str(endereco) + " conectou-se.")      # Mostra a mensagem no servidor que o IP X se conectou

        # Criação e execução da thread da função handle()
        t2 = threading.Thread(name="handle", target=handle, args=(cliente, endereco,))
        t2.start()
        time.sleep(0.2)                             # Delay da thread


# Criação e execução da thread da função receber()
t = threading.Thread(name="receber", target=receber)
t.start()


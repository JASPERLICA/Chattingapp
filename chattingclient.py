import threading
import socket


def receive_process(client):
    while True:
        try:
            message = client.recv(1024)
            print(message.decode())
        except :
            print("nothing received and return")
            return

if __name__ == "__main__":

    client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    host = socket.gethostname()
    # host = "127.0.0.1"
    port = 9909
    address = (host,port)

    client.connect(address)
    print(f"{port} has been connect")
    name = "Jasper"
    client.send(name.encode("utf-8"))
    # client.send(b"jasper")
    print(f"client sent name :{name} to server")
    client_thread = threading.Thread(target=receive_process,args=(client,),daemon=True)
    client_thread.start()
    while True:
        try:
            re_data = input()
            client.send(re_data.encode())
        except KeyboardInterrupt as e:
            print(e)
            break
    
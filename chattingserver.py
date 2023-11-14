# from socket import *
import socket
import threading


# from socket import socket


def send_one_client(to_socket, msg):
    if lock.acquire(socket_wait_lock_timeout):
        to_socket.send(msg.encode())
        lock.release()


def send_all_client(all_client_socket, msg):
    print("in the send all function")
    for individual_socket in all_client_socket:
        try:
            if lock.acquire(socket_wait_lock_timeout):
                individual_socket.send(msg.encode())
                lock.release()
        except:
            pass


def communication(client_socket, address):
    while True:
        try:
            data = client_socket.recv(1024)
            print(data.decode())
            msg = data.decode()
            from_name = name_address[str(address)]
            if msg.startswith("@"):
                index = msg.index(" ")
                print(f"index:{index}")
                to_name = msg[1:index]
                print(f"to_name:{to_name}")
                if to_name in name_clientsocket.keys():
                    to_socket = name_clientsocket[to_name]
                    print(f"to_socket:{to_socket}")
                    send_msg = msg[index:]
                    print(f"index:{index} to_name :{to_name} send_msg :{send_msg}")

                    send_one_client(to_socket, send_msg)
                    print(f"send to {to_name} message:{send_msg}")

                else:
                    print(f"no {to_name} in the group")
            else:
                print("send all start")
                send_all_client(all_client_socket, msg)
                print(f"send to everyone a message:{msg}")
        except Exception as e:
            print(e)
            name = name_address[str(address)]
            socket_to_del = name_clientsocket[name]
            all_client_socket.remove(socket_to_del)
            name_clientsocket.pop(name)
            del name_clientsocket[name]
            print(f"{name} exit from chating")
            print(f"new neme_client_socket{name_clientsocket}")
            print(f"new all_client_socket{all_client_socket}")
            return


if __name__ == '__main__':

    # clint name : address (ip port)
    name_address = {}
    # client name: socket
    name_clientsocket = {}
    # all client socket
    all_client_socket: list[socket] = []
    command_ask_name = "tpye your name"
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    host = socket.gethostname()
    # host = "127.0.0.1"
    port = 9909
    address = (host, port)
    server.bind(address)
    server.listen(10)
    lock = threading.Lock()
    socket_wait_lock_timeout = True
    while True:
        try:
            print(f'server socket listen to {port}')
            client_socket, address = server.accept()
            print(f"new client {address} join")
        # except Exception as e:
        #     print(e)
        except:
            break
        # server.send(command_ask_name.encode())
        try:
            data = client_socket.recv(1024)
            name = data.decode()
            name_address[str(address)] = name
            print(name_address)
            name_clientsocket[str(name)] = client_socket
            print(name_clientsocket)
            all_client_socket.append(client_socket)
            print(all_client_socket)

            client_thread = threading.Thread(target=communication, args=(client_socket, address), daemon=True)
            client_thread.start()
        except Exception as e:
            print(e)
            print("something worng")
            break
    print("end...")

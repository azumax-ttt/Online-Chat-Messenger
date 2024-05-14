import socket
import time

class ClientInfo:
    def __init__(self, address, username, message, received_time):
        self.address = address
        self.username = username
        self.message = message
        self.received_time = received_time

def send_message_to_other_members(sock, data, sender_addr, client_infos):
    for addr, info in client_infos.items():
        if addr != sender_addr:
            try:
                sock.sendto(data, info.address)
            except Exception as e:
                print(f"Error sending message: {e}")

def remove_inactive_clients(client_infos):
    delete_time = 100  # seconds
    current_time = time.time()
    keys_to_remove = [key for key, info in client_infos.items() if current_time - info.received_time > delete_time]
    for key in keys_to_remove:
        del client_infos[key]

def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_address = ('', 8080)
    sock.bind(server_address)
    print(f"Starting UDP server on {server_address}")

    client_infos = {}

    while True:
        data, addr = sock.recvfrom(4096)
        username_len = data[0]
        username = data[1:1+username_len].decode()
        message = data[1+username_len:].decode()

        print(f"Received from {addr}")
        print(f"username: {username}")
        print(f"message: {message}")

        if len(data) > 4096:
            continue

        send_message_to_other_members(sock, data, addr, client_infos)
        client_infos[addr] = ClientInfo(addr, username.encode(), message.encode(), time.time())
        remove_inactive_clients(client_infos)
        print(f"Number of clients: {len(client_infos)}\n")

if __name__ == "__main__":
    main()

import socket
import threading

def receive_messages(sock):
    while True:
        try:
            data, _ = sock.recvfrom(4096)
            username_len = data[0]
            username = data[1:1+username_len].decode()
            message = data[1+username_len:].decode()
            print(f"\nMessage from {username}: {message}")
            print("Enter message: ", end='', flush=True)
        except Exception as e:
            print(f"Error receiving message: {e}")
            break

def main():
    server_address = ('localhost', 8080)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    username = input("Enter username: ")
    encoded_username = username.encode()
    username_len = len(encoded_username)

    print(f"Starting chat with {username}")
    name_part = bytes([username_len]) + encoded_username

    receiver_thread = threading.Thread(target=receive_messages, args=(sock,))
    receiver_thread.start()

    while True:
        message = input("Enter message: ")
        encoded_message = message.encode()
        msg = name_part + encoded_message
        if len(msg) > 4096:
            print("Message too long")
            continue
        try:
            sock.sendto(msg, server_address)
        except Exception as e:
            print(f"Error sending message: {e}")
            break

if __name__ == "__main__":
    main()

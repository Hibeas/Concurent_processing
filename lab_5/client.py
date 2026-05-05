import socket
import threading
import os

def receive_handler(s):
    try:
        while True:
            data = s.recv(4096).decode('utf-8')
            if not data or data.lower() == "closed":
                print("\nServer sent 'closed'. Closing client...")
                os._exit(0)
            print(f"\n[SERVER]: {data}\nInput: ", end="")
    except Exception:
        os._exit(0)

def send_file(s, filename):
    if os.path.exists(filename):
        s.send(f"FILE:{filename}".encode('utf-8'))
        with open(filename, "rb") as f:
            while (chunk := f.read(4096)):
                s.sendall(chunk)
        s.send(b"EOF")
        print(f"Sent: {filename}")
    else:
        print(f"File {filename} not found.")

def start_client():
    HOST = '127.0.0.1'
    PORT = 1975 

    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((HOST, PORT))

        threading.Thread(target=receive_handler, args=(client,), daemon=True).start()

        while True:
            msg = input("Input: ")
            
            if msg.lower() == 'closed':
                client.send(msg.encode('utf-8'))
                break
            elif msg in ['text1.txt', 'text2.txt']:
                send_file(client, msg)
            else:
                client.send(msg.encode('utf-8'))
    except Exception as e:
        print(f"Error: {e}")
    finally:
        client.close()

if __name__ == "__main__":
    start_client()
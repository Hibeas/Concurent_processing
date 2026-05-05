import socket
import threading
import os

def handle_client(conn, addr):
    try:
        surname = "Skarbek"
        welcome_msg = f"I am a {surname} Server"
        conn.send(welcome_msg.encode('utf-8'))

        while True:
            data = conn.recv(4096).decode('utf-8')
            if not data:
                break
            if data.lower() == "closed":
                print(f"Client {addr} want closing.")
                break
            
            if data.startswith("FILE:"):
                filename = data.split(":")[1]
                with open(f"received_{filename}", "wb") as f:
                    while True:
                        bytes_read = conn.recv(4096)
                        if bytes_read.endswith(b"EOF"):
                            f.write(bytes_read[:-3])
                            break
                        f.write(bytes_read)
                print(f"File {filename} received successfully.")
            else:
                print(f"[{addr}] {data}")
    except Exception:
        pass
    finally:
        print(f"Connection with {addr} ended.")
        conn.close()

def server_input_handler(clients):
    while True:
        cmd = input()
        if cmd.lower() == "closed":
            print("Sending 'closed' to all clients and shutting down...")
            for c in clients:
                try:
                    c.send("closed".encode('utf-8'))
                except:
                    pass
            os._exit(0)

def start_server():
    HOST = '127.0.0.1'
    PORT = 1975 
    clients = []
    
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()
    print(f"Server active on {PORT}. Type 'closed' to shutdown.")

    threading.Thread(target=server_input_handler, args=(clients,), daemon=True).start()

    while True:
        try:
            conn, addr = server.accept()
            clients.append(conn)
            threading.Thread(target=handle_client, args=(conn, addr)).start()
        except Exception:
            break

if __name__ == "__main__":
    start_server()
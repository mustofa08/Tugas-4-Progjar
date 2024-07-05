import base64
import os
import socket
import threading

def handle_client(client_socket):
    try:
        request = client_socket.recv(1024).decode()
        command, *params = request.split(' ')

        if command == "UPLOAD":
            filename = params[0]
            file_content_base64 = ' '.join(params[1:])
            file_content = base64.b64decode(file_content_base64.encode())
            with open(filename, 'wb') as file:
                file.write(file_content)
            response = f"OK File {filename} uploaded successfully."
            
        elif command == "DELETE":
            filename = params[0]
            if os.path.exists(filename):
                os.remove(filename)
                response = f"OK File {filename} deleted successfully."
            else:
                response = f"ERROR File {filename} does not exist."
        else:
            response = "Error Invalid"

        client_socket.send(response.encode())
    except Exception as e:
        response = f"ERROR {str(e)}"
        client_socket.send(response.encode())
    finally:
        client_socket.close()

def start_server(server_ip, server_port):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((server_ip, server_port))
    server.listen(5)
    
    print(f"[*] Listening on {server_ip}:{server_port}")

    while True:
        client_socket, addr = server.accept()
        print(f"[*] Accepted connection from {addr[0]}:{addr[1]}")
        client_handler = threading.Thread(target=handle_client, args=(client_socket,))
        client_handler.start()

if __name__ == "__main__":
    start_server("0.0.0.0", 9999)

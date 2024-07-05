import base64
import socket

def send_request(request, server_ip, server_port):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client.connect((server_ip, server_port))
        client.send(request.encode())
        response = client.recv(4096).decode()
        return response
    except ConnectionRefusedError:
        return "ERROR Connection refused. Make sure the server is running."
    finally:
        client.close()

def delete_file(filename, server_ip, server_port):
    request = f"DELETE {filename}"
    return send_request(request, server_ip, server_port)

def upload_file(filename, server_ip, server_port):
    try:
        with open(filename, 'rb') as file:
            file_content = file.read()
        file_content_base64 = base64.b64encode(file_content).decode()
        request = f"UPLOAD {filename} {file_content_base64}"
        response = send_request(request, server_ip, server_port)
        return response
    except FileNotFoundError:
        return f"ERROR File not found."

if __name__ == "__main__":
    server_ip = input("Enter server IP address: ")
    server_port = 9999

    while True:
        command = input("Enter (UPLOAD <filename> / DELETE <filename> / EXIT): ")
        if command.startswith("UPLOAD "):
            filename = command.split(' ')[1]
            response = upload_file(filename, server_ip, server_port)
            print(response)
        elif command.startswith("DELETE "):
            filename = command.split(' ')[1]
            response = delete_file(filename, server_ip, server_port)
            print(response)
        elif command == "EXIT":
            break
        else:
            print("Error: Invalid command")

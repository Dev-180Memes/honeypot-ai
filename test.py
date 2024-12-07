import socket
import random
import time

def send_legitimate_request(ip, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((ip, port))

    # Create a legitimate request
    legitimate_request = "GET / HTTP/1.1\r\n"
    legitimate_request += f"User-Agent: NormalBrowser/{random.randint(1, 10)}\r\n"
    legitimate_request += "\r\n"

    s.sendall(legitimate_request.encode())
    time.sleep(random.randint(1, 5))  # Simulate random delays
    s.close()

if __name__ == '__main__':
    ip = 'localhost'  # Replace with your server's IP
    port = 2222  # Replace with your server's port

    # Send multiple legitimate requests
    for _ in range(10):
        send_legitimate_request(ip, port)
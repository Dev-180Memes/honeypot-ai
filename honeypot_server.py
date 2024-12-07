import socket
import time
import joblib
from preprocess import extract_features

clf = joblib.load('./weights/model.pkl')
scaler = joblib.load('./weights/scaler.pkl')
le = joblib.load('./weights/label_encoder.pkl')

def handle_connection(connection, address):
    connection_start_time = time.time()
    data_received = b''
    data_sent = b''
    try:
        while True:
            chunk = connection.recv(1024)
            if not chunk:
                break
            data_received += chunk
            response = b'HTTP/1.1 200 OK\r\nContent-Length: 0\r\n\r\n'
            connection.send(response)
            data_sent += response
    except Exception as e:
        print(f'Error: {e}')
    finally:
        connection.close()
        features = extract_features(connection_start_time, data_received, data_sent)
        features_scaled = scaler.transform([features])
        prediction = clf.predict(features_scaled)
        if prediction[0] == 1:
            print(f'Malicious activity detected from {address[0]}')
        else:
            print(f'Normal activity detected from {address[0]}')

        with open('honeypot_log.txt', 'a') as f:
            f.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - {address[0]} - {'Malicious' if prediction[0] == 1 else 'Benign'}\n")

def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ('localhost', 2222)
    server_socket.bind(server_address)
    server_socket.listen(5)
    print(f'Server started on {server_address[0]}:{server_address[1]}')
    while True:
        connection, client_address = server_socket.accept()
        handle_connection(connection, client_address)

if __name__ == '__main__':
    main()
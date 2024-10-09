import socket
import os

def send_music_to_client(client_socket, folder_path):
    # Listar todos os arquivos na pasta
    music_files = [f for f in os.listdir(folder_path) if f.endswith('.mp3')]
    
    # Enviar cada arquivo de música para o cliente
    for music_file in music_files:
        file_path = os.path.join(folder_path, music_file)
        print(f"Enviando: {music_file}")
        with open(file_path, 'rb') as f:
            data = f.read(4096)
            while data:
                client_socket.send(data)
                data = f.read(4096)
    
    client_socket.close()

def start_server(host='192.168.29.37', port=65432, folder_path='C:\\Musica'):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen()

    print(f"Servidor esperando conexões em {host}:{port}...")

    while True:
        client_socket, client_address = server_socket.accept()
        print(f"Cliente conectado: {client_address}")
        send_music_to_client(client_socket, folder_path)

if __name__ == "__main__":
    start_server(folder_path='C:\\Musica')
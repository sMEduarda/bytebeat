import socket
def send_music_to_client(client_socket, file_path):
    with open(f"C:\\Musica\\musica1.mp3", 'rb') as music_file:
        data = music_file.read(4096)
        while data:
            client_socket.send(data)
            data = music_file.read(4096)
    client_socket.close()

def start_server(host='192.168.29.56', port=65432, music_file='musica1.mp3)'):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen()

    print(f"Servidor esperando conexões em {host}:{port}...")

    while True:
        client_socket, client_address = server_socket.accept()
        print(f"Cliente conectado: {client_address}")
        send_music_to_client(client_socket, music_file)

if __name__ == "__main__":
    start_server(music_file= "C:\\Musica\\musica1.mp3")

import tkinter
import customtkinter
import pygame
from threading import Thread
import socket
import io
import os
import time
import math

customtkinter.set_appearance_mode("dark")  # Modes: system (default), light, dark
customtkinter.set_default_color_theme("dark-blue")  # Themes: blue (default), dark-blue, green

##### Tkinter setup ######
root = customtkinter.CTk()
root.title('Music Player')
root.geometry('400x480')
pygame.mixer.init()
##########################

# Função para receber a música do servidor
def receive_music_from_server(host='192.168.29.37', port=65432):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))

    music_data = b''
    while True:
        data = client_socket.recv(4096)
        if not data:
            break
        music_data += data

    client_socket.close()
    return music_data

# Função para tocar a música
def play_music_thread():
    global music_data, is_playing
    if music_data is None or len(music_data) == 0:
        print("Erro: Nenhum dado de música para reproduzir.")
        is_playing = False
        return

    # Criação do arquivo temporário no diretório de trabalho atual
    current_directory = os.path.dirname(os.path.abspath(__file__))
    temp_file = os.path.join(current_directory, 'temp_music.mp3')

    try:
        # Salva a música no diretório atual
        with open(temp_file, 'wb') as f:
            f.write(music_data)
        
        # Verifica se o arquivo foi criado com sucesso
        if os.path.exists(temp_file):  # Certifica-se de que o arquivo foi criado
            print(f"Arquivo {temp_file} salvo com sucesso.")
            pygame.mixer.music.load(temp_file)
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(10)
        else:
            print(f"Erro: Arquivo {temp_file} não encontrado.")
    except Exception as e:
        print(f"Erro ao tentar reproduzir a música: {e}")
    finally:
        is_playing = False
        # Após a reprodução, remove o arquivo temporário
        if os.path.exists(temp_file):
            os.remove(temp_file)

# Função para parar a música
def stop_music():
    global is_playing
    pygame.mixer.music.stop()
    is_playing = False
    print("Música parada.")

# Inicializa a música e o status de reprodução
music_data = receive_music_from_server()
is_playing = False

# Salva o arquivo recebido para depuração ou uso posterior
current_directory = os.path.dirname(os.path.abspath(__file__))
temp_music_path = os.path.join(current_directory, "countdown.mp3")

with open(temp_music_path, "wb") as f:
    f.write(music_data)

# Verifica se os dados de música foram recebidos corretamente
if not music_data:
    print("Erro: Nenhum dado de música recebido.")
else:
    print("Música recebida com sucesso!")

list_of_songs = [temp_music_path]  # Lista de músicas, a primeira será tocada
n = 0

# Função de progresso (apenas ilustrativa, sem relação direta com o problema atual)
def progress():
    a = pygame.mixer.Sound(f'{list_of_songs[n]}')
    song_len = a.get_length() * 3
    for i in range(0, math.ceil(song_len)):
        time.sleep(.4)

def threading_progress():
    t1 = Thread(target=progress)
    t1.start()

# Função para tocar a música atual
def play_music():
    global n
    if len(list_of_songs) > 0:
        song_name = list_of_songs[n]
        if os.path.exists(song_name):  # Verifica se o arquivo existe antes de tocar
            pygame.mixer.music.load(song_name)
            pygame.mixer.music.play(loops=0)
            pygame.mixer.music.set_volume(.5)
        else:
            print(f"Erro: Arquivo {song_name} não encontrado.")

# Função para ajustar o volume
def volume(value):
    pygame.mixer.music.set_volume(float(value))

# Botões
play_button = customtkinter.CTkButton(master=root, text='Play', command=play_music)
play_button.place(relx=0.5, rely=0.7, anchor=tkinter.CENTER)

# Botão "Stop"
stop_button = customtkinter.CTkButton(master=root, text='Stop', command=stop_music)
stop_button.place(relx=0.5, rely=0.85, anchor=tkinter.CENTER)

# Slider de volume
slider = customtkinter.CTkSlider(master=root, from_=0, to=1, command=volume, width=210)
slider.place(relx=0.5, rely=0.78, anchor=tkinter.CENTER)

root.mainloop()

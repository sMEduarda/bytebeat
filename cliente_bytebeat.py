import tkinter
from tkinter.ttk import Progressbar
import customtkinter
import pygame
from PIL import Image, ImageTk
from threading import Thread
import time
import math
import socket
import io
import os

# Configurações do CustomTkinter
customtkinter.set_appearance_mode("dark")  # Modos: system (padrão), light, dark
customtkinter.set_default_color_theme("dark-blue")  # Temas: blue (padrão), dark-blue, green

##### Tkinter stuff ######
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

def play_music_thread():
    global music_data, is_playing

    if music_data is None or len(music_data) == 0:
        print("Erro: Nenhum dado de música para reproduzir.")
        is_playing = False
        return

    music_stream = io.BytesIO(music_data)
    temp_file = 'temp_music.mp3'

    try:
        with open(temp_file, 'wb') as f:
            f.write(music_data)

        pygame.mixer.music.load(temp_file)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
    except Exception as e:
        print(f"Erro ao tentar reproduzir a música: {e}")
    finally:
        is_playing = False
        if os.path.exists(temp_file):
            os.remove(temp_file)

def play_music():
    global is_playing
    if not is_playing:
        is_playing = True
        play_thread = Thread(target=play_music_thread)
        play_thread.start()

def stop_music():
    global is_playing
    pygame.mixer.music.stop()
    is_playing = False
    print("Música parada.")

# Inicializa a música e o status de reprodução
music_data = receive_music_from_server()
is_playing = False

# Salva o arquivo recebido para depuração ou uso posterior
with open("countdown.mp3", "wb") as f:
    f.write(music_data)

list_of_songs = ['temp_music.mp3']  # Lista de músicas
n = 0

def progress():
    a = pygame.mixer.Sound(f'{list_of_songs[n]}')
    song_len = a.get_length() * 3
    for i in range(0, math.ceil(song_len)):
        time.sleep(0.4)

def threading_progress():
    t1 = Thread(target=progress)
    t1.start()

def skip_forward():
    global n
    if n < len(list_of_songs) - 1:
        n += 1
        play_music()

def skip_back():
    global n
    if n > 0:
        n -= 1
        play_music()

def volume(value):
    pygame.mixer.music.set_volume(float(value))

# Botões e controles da interface
play_button = customtkinter.CTkButton(master=root, text='Play', command=play_music)
play_button.place(relx=0.5, rely=0.7, anchor=tkinter.CENTER)

slider = customtkinter.CTkSlider(master=root, from_=0, to=1, command=volume, width=210)
slider.place(relx=0.5, rely=0.78, anchor=tkinter.CENTER)

root.mainloop()

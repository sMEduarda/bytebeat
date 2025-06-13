import tkinter
from tkinter.ttk import Progressbar
import customtkinter
import pygame
from PIL import Image, ImageTk
from threading import *
import time
import math
import socket
import io
import os
import time 
import math

customtkinter.set_appearance_mode("dark")  # Modes: system (default), light, dark
customtkinter.set_default_color_theme("dark-blue")  # Themes: blue (default), dark-blue, green

##### Tkinter stuff ######
root = customtkinter.CTk()
root.title('Music Player')
root.geometry('400x480')
pygame.mixer.init()
##########################


def receive_music_from_server(host='192.168.29.56', port=65432):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))

    music_data = b'temp_music'
    while True:
        data = client_socket.recv(4096)
        if not data:
            break
        music_data += data

    client_socket.close()
    return music_data

def play_music():
    global music_data, is_playing
    if not is_playing:
        is_playing = True
        play_thread = threading.Thread(target=play_music_thread)
        play_thread.start()

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
        
        # Tenta tocar o arquivo MP3
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

def stop_music():
    global is_playing
    pygame.mixer.music.stop()
    is_playing = False
    print("Música parada.")

def pause_music():
    print("Pausa não suportada diretamente com pygame.")

# Inicializa a música e o status de reprodução
music_data = receive_music_from_server()
is_playing = False

# Salva o arquivo recebido para fins de depuração ou uso posterior
with open("countdown.mp3", "wb") as f:
    f.write(music_data)

# Verifica se os dados de música foram recebidos
if not music_data:
    print("Erro: Nenhum dado de música recebido.")


list_of_songs = ['temp_music.mp3'] # Add more songs into this list, make sure they are .wav and put into the music Directory.
n = 0

def progress():
    a = pygame.mixer.Sound(f'{list_of_songs[n]}')
    song_len = a.get_length() * 3
    for i in range(0, math.ceil(song_len)):
        time.sleep(.4)
        

def threading():
    t1 = Thread(target=progress)
    t1.start()

def play_music():
    threading()
    global n 
    current_song = n
    if n > 2:
        n = 0
    song_name = list_of_songs[n]
    pygame.mixer.music.load(song_name)
    pygame.mixer.music.play(loops=0)
    pygame.mixer.music.set_volume(.5)

    # print('PLAY')
    n += 1

def skip_forward():
    # As an idea, you can turn play_music() into a start/pause function and create a seperate skip ahead function for this!
    play_music()

def skip_back():
    global n
    n -= 2
    play_music()

def volume(value):
    #print(value) # If you care to see the volume value in the terminal, un-comment this :)
    pygame.mixer.music.set_volume(value)


# All Buttons
play_button = customtkinter.CTkButton(master=root, text='Play', command=play_music)
play_button.place(relx=0.5, rely=0.7, anchor=tkinter.CENTER)

slider = customtkinter.CTkSlider(master=root, from_= 0, to=1, command=volume, width=210)
slider.place(relx=0.5, rely=0.78, anchor=tkinter.CENTER)

root.mainloop()

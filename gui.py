#pyinstaller --onefile --icon=brainstorm.ico --add-data "brainstorm.ico;." --name "music_bingo" gui.py
#pyinstaller --onefile --icon=brainstorm.ico  musicbingo.spec

#icon from https://www.flaticon.com/premium-icon/music_1014256?term=music&page=1&position=18&page=1&position=18&related_id=1014256&origin=search
import tkinter
from tkinter import *
from tkinter_custom_button import TkinterCustomButton
from PIL import Image, ImageTk
import os
import threading
import json
from music import *
from bingo import *

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller
    https://stackoverflow.com/questions/7674790/bundling-data-files-with-pyinstaller-onefile"""
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def shuffle():
    print("Shuffle!")
    my_player.shuffle()
    update_lists()
    calculate_bingo()

def next():
    if not my_player.playing:
        thread = threading.Thread(target=play_next)
        thread.start()
    update_lists()

def back():
    my_player.back()
    update_lists()

def play_next():
    my_player.play_next_song()
    #calculate_bingo()

def update_lists():
    queueText['text']  = "Queue: "+str(my_player.queue)
    playedText['text'] = "Played: "+str(my_player.played)

def refresh_lists():
    while True:
        time.sleep(5)
        if len(my_player.queue) > 0 and len(my_player.played) > 0:
            update_lists()

def calculate_bingo():
    bingo_boards.find_bingo(my_player.played,my_player.queue)

# Define our switch function
def switch():
    global is_on
    # Determine is on or off
    if is_on:
        autoplayButton.config(image = off)
        is_on = False
        my_player.set_autoplay(False)
    else:
        autoplayButton.config(image = on)
        is_on = True
        my_player.set_autoplay(True)

path = 'audio/'
#path = '/home/artur/Desktop/DadStuff/MusicBingo/audio/1'

with open('bingo.json') as f:
#with open('/home/artur/Desktop/DadStuff/MusicBingo/bingo.json') as f:
  bingo_json = json.load(f)

num_songs   = bingo_json['num_songs']
board_sides = bingo_json['board_sides']
num_players = bingo_json['num_players']
boards = [board['board'] for board in bingo_json['boards']]

boards_start = 0 #First board given away
boards_end = 20  #Highest board given away + 1

boards = boards[boards_start:boards_end]
my_player = SongPlayer(path,num_songs)
bingo_boards = Bingo(boards)
calculate_bingo()

root = Tk()
root.geometry('800x1000')
#root.iconbitmap(resource_path("brainstorm.ico"))

background_image= PhotoImage(file=resource_path("test.png"))
background_label = Label(root, image=background_image)
background_label.place(x=0, y=0)

on = PhotoImage(file = resource_path("on.png"))
off = PhotoImage(file = resource_path("off.png"))
is_on = True

root.grid_rowconfigure(0, weight=1)
root.grid_rowconfigure(2, weight=1)
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(2, weight=1)

#play_image = ImageTk.PhotoImage(Image.open("button_images/play.png").resize((40, 40)))
#skip_image = ImageTk.PhotoImage(Image.open("button_images/next.png").resize((40, 40)))

title = Label(root, text="Music Bingo", font=("Verdana", 30))
title.place(relx=0.5, rely=0.1, anchor=tkinter.CENTER)

queueText = Label(root, text="Queue: "+str(my_player.queue), font=("Verdana", 15),wraplength=300)
queueText.place(relx=0.5, rely=0.3, anchor=tkinter.CENTER)

playedText = Label(root, text="Played: "+str(my_player.played), font=("Verdana", 15),wraplength=300)
playedText.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

autoplayText = Label(root, text="Autoplay:", font=("Verdana", 15))
autoplayText.place(relx=0.40, rely=0.90, anchor=tkinter.CENTER)
autoplayButton = Button(root, image = on, bd = 0,command = switch)
autoplayButton.place(relx=0.55, rely=0.90, anchor=tkinter.CENTER)

backButton = TkinterCustomButton(text="Back", corner_radius=10, command=back)
backButton.place(relx=0.2, rely=0.80, anchor=tkinter.CENTER)

shuffleButton = TkinterCustomButton(text="Shuffle", command=shuffle)
shuffleButton.place(relx=0.5, rely=0.80, anchor=tkinter.CENTER)

nextButton = TkinterCustomButton(text="Play", command=next)
nextButton.place(relx=0.8, rely=0.80, anchor=tkinter.CENTER)

refresh_lists_thread = threading.Thread(target=refresh_lists)
refresh_lists_thread.start()

if __name__ == "__main__":
    root.mainloop()

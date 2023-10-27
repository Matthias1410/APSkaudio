# img_viewer.py

import PySimpleGUI as sg
from PIL import Image, ImageTk
import os.path
import time
import threading
import io
from PIL import Image

import funkcje
import pyperclip

# First the window layout in 2 columns

def update_counter(window):
    i = 0
    while True:
        window["-licznik-"].update(i)
        time.sleep(1)
        i += 1

def display_gif(filename, window):
    try:
        gif = Image.open(filename)
        frames = []
        durations = []
        for frame in range(gif.n_frames):
            gif.seek(frame)
            resized_frame = gif.copy()
            #resized_frame.thumbnail((200, 200))  # Dostosuj rozmiar klatek
            frame_data = ImageTk.PhotoImage(resized_frame)
            frames.append(frame_data)
            durations.append(gif.info['duration'])

        current_frame = 0
        playing_gif = True  # Zmienna określająca, czy GIF jest odtwarzany

        while True:
            if playing_gif:
                window['-IMAGE-'].update(data=frames[current_frame % len(frames)])
                current_frame += 1
            event, values = window.read(timeout=durations[current_frame % len(frames)])

            if event in (sg.WIN_CLOSED, 'Exit'):
                break
            elif event == "-FILE LIST-":  # Zresetuj odtwarzanie GIF po wybraniu nowego pliku
                playing_gif = False
                filename = os.path.join(values["-FOLDER-"], values["-FILE LIST-"][0])
                window["-TOUT-"].update(filename)
                if filename.lower().endswith('.gif'):
                    print("pew")
                    display_gif(filename, window) 
                    event="-FILE LIST-"
                elif filename.lower().endswith('png'):           
                    window["-IMAGE-"].update(filename=filename)
                else:
                    muzyczka(filename)
                break

    except Exception as e:
        print(f"Error: {e}")
        
        
file_list_column = [
    [sg.Text("Licznik od momentu startu"),sg.Text("Jakasliczba",key="-licznik-"),],
    [
        sg.Text("Image Folder"),

        sg.In(size=(25, 1), enable_events=True, key="-FOLDER-"),
        sg.FolderBrowse(),
    ],
    [
        sg.Listbox(
            values=[], enable_events=True, size=(40, 20), key="-FILE LIST-"
        )
    ],
]

# For now will only show the name of the file that was chosen
image_viewer_column = [
    [sg.Text("Choose an .wav file on the left")],
    [sg.Text(size=(40, 1), key="-TOUT-")],
    [sg.Text("Text to code",size=(15, 1)), sg.InputText(key="-INPUT-",size=(20, 15))],
    [sg.Text("outputname",size=(15, 1)), sg.InputText(key="-OUTPUT-",size=(20, 15))],
    [sg.Button("Zakoduj wiadomosc",key="4", enable_events=True,size=(10, 2)),sg.Button("Odkoduj",key="5", enable_events=True,size=(10, 2))],
    [sg.Text("Wynik dekodowanie",size=(15, 1)),sg.InputText(key="-WYNIK-",size=(20, 15))],
    [sg.Text(size=(20, 5),key="-TEXT-")],
    
]

# ----- Full layout -----
layout = [
    [
        sg.Column(file_list_column),
        sg.VSeperator(),
        sg.Column(image_viewer_column),
    ]
]


window = sg.Window("APskaudio", layout, resizable=True, finalize=True)

# Run the Event Loop

thread = threading.Thread(target=update_counter, args=(window,), daemon=True)
thread.start()
licznik=0    
while True:
    event, values = window.read(timeout=1000)
    

    
    if event == "Exit" or event == sg.WIN_CLOSED:
        break
    # Folder name was filled in, make a list of files in the folder
    if event == "-FOLDER-":
        folder = values["-FOLDER-"]
        try:
            # Get list of files in folder
            file_list = os.listdir(folder)
        except:
            file_list = []

        fnames = [
            f
            for f in file_list
            if os.path.isfile(os.path.join(folder, f))
            and f.lower().endswith(("wav"))
        ]
        window["-FILE LIST-"].update(fnames)
    elif event == "-FILE LIST-":  # A file was chosen from the listbox     
        try:
            filename = os.path.join(values["-FOLDER-"], values["-FILE LIST-"][0])
            window["-TOUT-"].update(filename)
        except:
            pass
    elif event == "4":
        try:
            dane=values['-INPUT-']
            outputname=values['-OUTPUT-']
            print(dane,outputname)
            funkcje.hidemessage(filename,dane,outputname)
        except:
            pass
    elif event == "5":
        try:
            dane=funkcje.discovermessage(filename)
            window["-WYNIK-"].update(dane)
        except:
            pass
          


window.close()
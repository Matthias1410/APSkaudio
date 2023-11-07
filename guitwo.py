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
        
'''        
file_list_column = [
    [sg.Button("Back to Main Menu",key="MAIN_menu", enable_events=True,size=(20, 2))],
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
main_menu_options = [
    [sg.Button("Tryb LSB",key="LSB_button", enable_events=True,size=(10, 2)),sg.Button("Tryb Drugi",key="TWO_button", enable_events=True,size=(10, 2))],
    [sg.Button("Exit",key="EXIT_button", enable_events=True,size=(10, 2))],
    
    ]


# ----- Full layout -----
layout1 = [
    [
    sg.Column(main_menu_options)
    
    ]
]

layout2 = [
    [
        sg.Column(file_list_column),
        sg.VSeperator(),
        sg.Column(image_viewer_column),
    ]
]
'''





window1, window2, window3 = funkcje.make_window1(), None, None

#window = sg.Window("APskaudio", layout1, resizable=True, finalize=True)
modeLSB=1
while True:
    window, event, values = sg.read_all_windows()
    
    
    #dzialanie na window 1
    if window==window1:
        if event == "LSB_button":
            window1.hide()
            window2=funkcje.make_window2()
        if event == "TWO_button":
            window1.hide()
            window3=funkcje.make_window3()
        if event == "EXIT_button":
            break
    
            
            
    #dzialania na window 2
    if window == window2:
        #cofniecie do main menu
        if event == "MAIN_menu":
            window2.hide()
            window1.un_hide()
    # Reszta okna 2
        if event=="MODE_ONE":
            modeLSB=1
            print(modeLSB)
        elif event=="MODE_TWO":
            modeLSB=2
            print(modeLSB)
        elif event=="MODE_THREE":
            modeLSB=3
            print(modeLSB)
        
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
                funkcje.hidemessage(filename,dane,outputname,modeLSB)
            except:
                pass
        elif event == "5":
            try:
                dane=funkcje.discovermessage(filename,1,window)
                window["-WYNIK-"].update(dane)
            except:
                pass
    #dzialania na window 3
    if window==window3:
        print("xddd")


window.close()

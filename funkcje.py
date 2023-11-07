
import wave
import sys
import PySimpleGUI as sg

def kwadrat(number):
    if isinstance(number, int):
        i=number*number
        return i
    else:
        return("no chyba ci sie pomylilo", number,"is not an integer")
        

def make_window1():
    layout = [
        [sg.Button("Tryb LSB",key="LSB_button", enable_events=True,size=(10, 2)),sg.Button("Tryb Drugi",key="TWO_button", enable_events=True,size=(10, 2))],
        [sg.Button("Exit",key="EXIT_button", enable_events=True,size=(10, 2))],
    ]
    return sg.Window('Window 1', layout, finalize=True)


def make_window2():
    file_list_column = [
        [sg.Button("Back to Main Menu",key="MAIN_menu", enable_events=True,size=(20, 2))],
        [sg.Button("Jeden bit",key="MODE_ONE", enable_events=True,size=(10, 2)),sg.Button("Dwa bity",key="MODE_TWO", enable_events=True,size=(10, 2)),sg.Button("Trzy bity",key="MODE_THREE", enable_events=True,size=(10, 2))],
        [
            sg.Text("Sound Folder"),
            sg.In(size=(25, 1), enable_events=True, key="-FOLDER-"),
            sg.FolderBrowse(),
        ],
        [
            sg.Listbox(
                values=[], enable_events=True, size=(40, 20), key="-FILE LIST-"
            )
        ],
    ]
    image_viewer_column = [
        [sg.Text("Choose an .wav file on the left")],
        [sg.Text(size=(40, 1), key="-TOUT-")],
        [sg.Text("Text to code",size=(15, 1)), sg.Multiline(key="-INPUT-",size=(20, 10))],
        [sg.Text("outputname",size=(15, 1)), sg.InputText(key="-OUTPUT-",size=(20, 15))],
        [sg.Button("Zakoduj wiadomosc",key="4", enable_events=True,size=(10, 2)),sg.Button("Odkoduj",key="5", enable_events=True,size=(10, 2))],
        [sg.Text("Wynik dekodowanie",size=(15, 1)),sg.Multiline(key="-WYNIK-",size=(20, 10))],
        [sg.Text(size=(20, 5),key="-TEXT-")],
    
    ]
    
    
    layout = [
        [
            sg.Column(file_list_column),
            sg.VSeperator(),
            sg.Column(image_viewer_column),
        ]
    ]

    return sg.Window('Window 2', layout, finalize=True)
    
def make_window3():
    print("xddd")
    
    

# Use wave package (native to Python) for reading the received audio file
def discovermessage(file,tryb):
    print("pls i need help")
    song = wave.open(file, mode='rb')
# Convert audio to byte array
    frame_bytes = bytearray(list(song.readframes(song.getnframes())))

# Extract the LSB of each byte
    extracted1 = [frame_bytes[i] & 1 for i in range(len(frame_bytes))]
    print("extracted1")
    #extracted2 = [frame_bytes[i] & 2 for i in range(len(frame_bytes))]
    #print("extracted 2")
    #extracted3 = [frame_bytes[i] & 3 for i in range(len(frame_bytes))]
    #print("extracted 3")
# Convert byte array back to string
    string = "".join(chr(int("".join(map(str,extracted1[i:i+8])),2)) for i in range(0,len(extracted1),8))
# Cut off at the filler characters
    decoded = string.split("###")[0]

# Print the extracted text
    song.close()
    print("Sucessfully decoded")
    return(decoded)
    
def hidemessage(file,string,output,tryb):
    print("odpalam hide message, filename=",file)
# read wave audio file
    song = wave.open(file, mode='rb')
# Read frames and convert to byte array
    frame_bytes = bytearray(list(song.readframes(song.getnframes())))

# The "secret" text message
# Append dummy data to fill out rest of the bytes. Receiver shall detect and remove these characters.
    string = string + int((len(frame_bytes)-(len(string)*8*8))/8) *'#'
# Convert text to bit array
    bits = list(map(int, ''.join([bin(ord(i)).lstrip('0b').rjust(8,'0') for i in string])))

# Replace LSB of each byte of the audio data by one bit from the text bit array
    if tryb == 1:
        for i, bit in enumerate(bits):
            frame_bytes[i] = (frame_bytes[i] & 254) | bit
    if tryb == 2:
        for i, bit in enumerate(bits):
            if i%2==1:
                frame_bytes[i] = (frame_bytes[i] & 254) | bit
            if i%2==0:
                frame_bytes[i] = (frame_bytes[i] & 253) | bit
    if tryb == 3:
        for i, bit in enumerate(bits):
            if i%3==2:
                frame_bytes[i] = (frame_bytes[i] & 254) | bit
            if i%3==1:
                frame_bytes[i] = (frame_bytes[i] & 253) | bit
            if i%3==0:
                frame_bytes[i] = (frame_bytes[i] & 251) | bit
# Get the modified bytes
    frame_modified = bytes(frame_bytes)
    new_file=output 
    print("Za new file:", new_file)
# Write bytes to a new wave audio file
    with wave.open(new_file, 'wb') as fd:
        fd.setparams(song.getparams())
        fd.writeframes(frame_modified)
    song.close()

    print("New Audio file is created and saved")

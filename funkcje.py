
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
        [sg.Button("Tryb LSB",key="LSB_button", expand_x=True,expand_y=True, enable_events=True,size=(20, 4)),sg.Button("Tryb Drugi",key="TWO_button",expand_x=True,expand_y=True, enable_events=True,size=(20, 4))],
        [sg.Button("Exit",key="EXIT_button", expand_x=True,expand_y=True, enable_events=True,size=(40, 4))],
    ]
    return sg.Window('Window 1', layout, resizable=True, finalize=True)


def make_window2():
    file_list_column = [
        [sg.Button("Back to Main Menu",key="MAIN_menu",expand_x=True, enable_events=True,size=(20, 2))],
        [sg.Button("Jeden bit",key="MODE_ONE",expand_x=True, enable_events=True,size=(10, 2)),sg.Button("Dwa bity",key="MODE_TWO",expand_x=True, enable_events=True,size=(10, 2)),sg.Button("Trzy bity",key="MODE_THREE",expand_x=True, enable_events=True,size=(10, 2))],
        [
            sg.Text("Sound Folder"),
            sg.In(size=(25, 1),expand_x=True, enable_events=True, key="-FOLDER-"),
            sg.FolderBrowse(),
        ],
        [
            sg.Listbox(
                values=[], enable_events=True, expand_x=True,expand_y=True, size=(40, 20), key="-FILE LIST-"
            )
        ],
    ]
    image_viewer_column = [
        [sg.Text("Choose an .wav file on the left")],
        [sg.Text(size=(40, 1), key="-TOUT-")],
        [sg.Text("Text to code",size=(15, 1)), sg.Multiline(key="-INPUT-",size=(20, 10),expand_x=True,expand_y=True)],
        [sg.Text("outputname",size=(15, 1)), sg.InputText(key="-OUTPUT-",size=(20, 15),expand_x=True)],
        [sg.Button("Zakoduj wiadomosc",key="4",expand_x=True,expand_y=True, enable_events=True,size=(10, 2)),sg.Button("Odkoduj",key="5", expand_x=True,expand_y=True,enable_events=True,size=(10, 2)),sg.Text("Rezultat",size=(15, 1),key="RESULT")],
        [sg.Text("Wynik dekodowanie",size=(15, 1)),sg.Multiline(key="-WYNIK-",size=(20, 10),expand_x=True,expand_y=True)],
        #[sg.Text(size=(20, 5),key="-TEXT-")],
    
    ]
    col1=sg.Column(file_list_column)
    col2=sg.Column(image_viewer_column)
    layout = [
        [
            col1,
            sg.VSeperator(),
            col2,
        ]
    ]
    okno=sg.Window('Window 2', layout, resizable=True, finalize=True)
    col1.expand(True, True)
    col2.expand(True, True)
    return okno
    
def make_window3():
    file_list_column = [
        [sg.Button("Back to Main Menu",key="MAIN_menu",expand_x=True, enable_events=True,size=(20, 2))],
        [
            sg.Text("Sound Folder"),
            sg.In(size=(25, 1),expand_x=True, enable_events=True, key="-FOLDER-"),
            sg.FolderBrowse(),
        ],
        [
            sg.Listbox(
                values=[], enable_events=True, size=(40, 20),expand_x=True,expand_y=True, key="-FILE LIST-"
            )
        ],
    ]
    image_viewer_column = [
        [sg.Text("Choose an .midi file on the left")],
        [sg.Text(size=(40, 1), key="-TOUT-")],
        [sg.Text("Text to code",size=(15, 1)), sg.Multiline(key="-INPUT-",size=(20, 10),expand_x=True,expand_y=True,)],
        [sg.Text("outputname",size=(15, 1)), sg.InputText(key="-OUTPUT-",size=(20, 15),expand_x=True)],
        [sg.Button("Zakoduj wiadomosc",key="4", enable_events=True,size=(10, 2),expand_x=True),sg.Button("Odkoduj",key="5", enable_events=True,size=(10, 2),expand_x=True),sg.Text("Rezultat",size=(15, 1),key="RESULT")],
        [sg.Text("Wynik dekodowanie",size=(15, 1)),sg.Multiline(key="-WYNIK-",size=(20, 10),expand_x=True,expand_y=True,)],
        #[sg.Text(size=(20, 5),key="-TEXT-")],
    
    ]
    
    col1=sg.Column(file_list_column)
    col2=sg.Column(image_viewer_column)
    layout = [
        [
            col1,
            sg.VSeperator(),
            col2,
        ]
    ]
    okno=sg.Window('Window 3', layout, resizable=True, finalize=True)
    col1.expand(True, True)
    col2.expand(True, True)
    return okno
    
    

# Use wave package (native to Python) for reading the received audio file
def discovermessage(file,window):
    print("pls i need help")
    try:    
        song = wave.open(file, mode='rb')
    except:
        window["RESULT"].update("Failed to open file")
        return ("FAIL")
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
    if ('###') in string:
        decoded = string.split("###")[0]
        window["RESULT"].update("Success")
    else:
        window["RESULT"].update("Failure")
        return ("FAIL")
    

# Print the extracted text
    song.close()
    print("Sucessfully decoded")
    return(decoded)
    
def hidemessage(file,string,output,tryb):
    output="out\\"+output+".wav"
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

import pydub
import pydub.playback
import wave
import sys


def kwadrat(number):
    if isinstance(number, int):
        i=number*number
        return i
    else:
        return("no chyba ci sie pomylilo", number,"is not an integer")
        
        
def muzyczka(plik):
    a = pydub.AudioSegment.from_mp3('plik')
    pydub.playback.play(a)
    
    

# Use wave package (native to Python) for reading the received audio file
def discovermessage(file):
    song = wave.open(file, mode='rb')
# Convert audio to byte array
    frame_bytes = bytearray(list(song.readframes(song.getnframes())))

# Extract the LSB of each byte
    extracted = [frame_bytes[i] & 1 for i in range(len(frame_bytes))]
# Convert byte array back to string
    string = "".join(chr(int("".join(map(str,extracted[i:i+8])),2)) for i in range(0,len(extracted),8))
# Cut off at the filler characters
    decoded = string.split("###")[0]

# Print the extracted text
    song.close()
    print("Sucessfully decoded")
    return(decoded)
    
def hidemessage(file,string,output):
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
    for i, bit in enumerate(bits):
        frame_bytes[i] = (frame_bytes[i] & 254) | bit
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
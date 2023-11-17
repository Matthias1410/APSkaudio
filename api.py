from helpers import *
from model import detangle, gen_loop

def m_encode(message, filename):
    filename=filename+".midi"
    encoded_message=kerasify(encode(message))
    #model integration
    encoded_message=gen_loop(encoded_message)
    #print(encoded_message)
    #
    return notes_to_midi(encoded_message, filename, instrument_name="Acoustic Grand Piano")
    #Acoustic Grand Piano


def m_decode(filename):
    encoded_message=midi_to_notes(filename)
    #model integration
    #print(encoded_message)
    encoded_message=detangle(encoded_message)
    #
    encoded_message=dekerasify(encoded_message)
    decoded_message=decode(encoded_message)
    return decoded_message


#m_encode("ala ma kota", "test2")
#print(m_decode("test2.midi"))
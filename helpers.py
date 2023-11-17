import pretty_midi
import random
import pandas as pd
import numpy as np
import collections

cipher=[["a","b","c","d","e","f","g","h"],["i","j","k","l","m","n","o","p"],["q","r","s","t","u","v","w","x"],["y","z"," ","0","","","",""]]



def encode(message):
    msgarray=[char for char in message]
    msgarray.append("0")
    pitches=[]
    durations=[]
    octave=random.randint(4,12)
    ctr=2
    pitches.append(2+octave*8)
    durations.append(3+random.randint(0,49)/100)
    pitches.append(3+octave*8)
    durations.append(3+random.randint(0,49)/100)
    for i in msgarray:
        if len(pitches)!=len(durations) or len(pitches)!=ctr:
            print("Illegal characters")
            return 0
        
        for a in range(4):
            for b in range(8):
                if cipher[a][b]==i:
                    shift=random.randint(0,49)/100
                    pitches.append(b+8*octave)
                    durations.append(a+shift)
        ctr+=1

    encoded_message=pitches,durations
    return encoded_message



def decode(encoded_message, window):
    pitches, durations=encoded_message
    octave=(pitches[0]-(pitches[0]%8))/8
    message=""
    started=False


    for a in range(len(durations)):
        durations[a]=int(durations[a])

    for i in range(len(pitches)):
        try:
            if cipher[durations[i]][pitches[i]%8]=="0":
                if started:
                    window["RESULT"].update("Success")
                    return message
                started=True
            if started and not cipher[durations[i]][pitches[i]%8]=="0" :
                message=message+cipher[durations[i]][pitches[i]%8]
        except:
            window["RESULT"].update("Failure")
            return "FAIL"
        
    window["RESULT"].update("Failure")
    return "FAIL"

def midi_to_notes(midi_file: str) -> pd.DataFrame:
  pm = pretty_midi.PrettyMIDI(midi_file)
  instrument = pm.instruments[0]
  notes = collections.defaultdict(list)

  # Sort the notes by start time
  sorted_notes = sorted(instrument.notes, key=lambda note: note.start)
  prev_start = sorted_notes[0].start

  for note in sorted_notes:
    start = note.start
    end = note.end
    notes['pitch'].append(note.pitch)
    notes['start'].append(start)
    notes['end'].append(end)
    notes['step'].append(start - prev_start)
    notes['duration'].append(end - start)
    prev_start = start

  return pd.DataFrame({name: np.array(value) for name, value in notes.items()})



def notes_to_midi(
  notes: pd.DataFrame,
  out_file: str, 
  instrument_name: str,
  velocity: int = 100,  # note loudness
) -> pretty_midi.PrettyMIDI:

  pm = pretty_midi.PrettyMIDI()
  instrument = pretty_midi.Instrument(
      program=pretty_midi.instrument_name_to_program(
          instrument_name))

  prev_start = 0
  for i, note in notes.iterrows():
    start = float(prev_start + note['step'])
    end = float(start + note['duration'])
    note = pretty_midi.Note(
        velocity=velocity,
        pitch=int(note['pitch']),
        start=start,
        end=end,
    )
    instrument.notes.append(note)
    prev_start = start

  pm.instruments.append(instrument)
  pm.write(out_file)
  return pm



def kerasify(encoded_message):
    pitches, durations=encoded_message
    notes=collections.defaultdict(list)
    prev_start=0.0
    prev_dur=0.0

    for i in range(len(pitches)):
        start=prev_start+prev_dur
        duration=durations[i]
        step=duration

        notes['pitch'].append(pitches[i])
        notes['start'].append(start)
        notes['end'].append(start+duration)
        notes['step'].append(duration)
        notes['duration'].append(duration)
        prev_start=start
        prev_dur=duration        

    return pd.DataFrame({name: np.array(value) for name, value in notes.items()})



def dekerasify(notes):
    pitches=[]
    durations=[]
    for i in range(len(notes)):
        pitches.append(notes['pitch'][i])
        durations.append(notes['step'][i])
    dekerasified=pitches, durations
    return dekerasified



#print(decode(encode("ala ma kota")))
#df=kerasify(encode("ala ma kota"))
#print(df)
#print(decode(dekerasify(df)))

#pm=notes_to_midi(df, out_file="bitchpog.midi", instrument_name="Acoustic Grand Piano")
#print(midi_to_notes("bitchpog.midi"))
#print(decode(dekerasify(midi_to_notes("bitchpog.midi"))))

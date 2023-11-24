import collections
import datetime
import fluidsynth
import glob
import numpy as np
import pathlib
import pandas as pd
import pretty_midi
import seaborn as sns
import tensorflow as tf
import random
import pickle
import os

from IPython import display
from matplotlib import pyplot as plt
from typing import Optional
from helpers import dekerasify



def predict_next_note(
    notes: np.ndarray, 
    model: tf.keras.Model, 
    temperature: float = 1.0) -> tuple[int, float, float]:
  """Generates a note as a tuple of (pitch, step, duration), using a trained sequence model."""

  assert temperature > 0

  # Add batch dimension
  inputs = tf.expand_dims(notes, 0)

  predictions = model.predict(inputs)
  pitch_logits = predictions['pitch']
  step = predictions['step']
  duration = predictions['duration']

  pitch_logits /= temperature
  pitch = tf.random.categorical(pitch_logits, num_samples=1)
  pitch = tf.squeeze(pitch, axis=-1)
  duration = tf.squeeze(duration, axis=-1)
  step = tf.squeeze(step, axis=-1)

  # `step` and `duration` values should be non-negative
  step = tf.maximum(0, step)
  duration = tf.maximum(0, duration)

  return int(pitch), float(step), float(duration)


def mse_with_positive_pressure(y_true: tf.Tensor, y_pred: tf.Tensor):
  mse = (y_true - y_pred) ** 2
  positive_pressure = 10 * tf.maximum(-y_pred, 0.0)
  return tf.reduce_mean(mse + positive_pressure)



def get_model():
    custom_objects={"my_package>mse_with_positive_pressure": mse_with_positive_pressure}

    with tf.keras.saving.custom_object_scope(custom_objects):
        filepath=os.path.join(os.path.abspath(os.path.dirname(__file__)), 'steganet525.h5')
        #model=tf.keras.models.load_model("steganet5.h5")
        model=tf.keras.models.load_model(filepath)
    return model



def gen_loop(notes):
    filepath=os.path.join(os.path.abspath(os.path.dirname(__file__)), 'dataset_file.pkl')
    with open(filepath, 'rb') as f:
        dataset = pickle.load(f)
    key_order = ['pitch', 'step', 'duration']
    #tnotes=np.stack([notes[key] for key in key_order], axis=1)
    tnotes=np.stack([dataset[key] for key in key_order], axis=1)
    input_notes=(tnotes[:25]/np.array([128,1,1]))
    generated_notes=[]
    ctr=0
    prev_start=0.0
    temperature=2.0
    model=get_model()

    for i in range(len(notes)*4):
        if i%4==0:
            try:
                pitch=notes['pitch'][ctr]
                step=notes['step'][ctr]
                duration=notes['step'][ctr]
                start=prev_start+step
                end=start+duration
                input_note=(pitch,step,duration)
                generated_notes.append((*input_note,start,end))
                input_notes=np.delete(input_notes,0,axis=0)
                input_notes=np.append(input_notes, np.expand_dims(input_note, 0), axis=0)
                prev_start=start

                ctr+=1
            except:
                pass
       
        else:
            pitch, step, duration = predict_next_note(input_notes, model, temperature)
            step=step+random.randint(1,50)/100
            start = prev_start + step
            duration=duration+random.randint(1,50)/100
            end = start + duration
            input_note = (pitch, step, duration)
            generated_notes.append((*input_note, start, end))
            input_notes = np.delete(input_notes, 0, axis=0)
            input_notes = np.append(input_notes, np.expand_dims(input_note, 0), axis=0)
            prev_start = start
    
    return pd.DataFrame(generated_notes, columns=(*key_order, 'start', 'end'))



def detangle(notes):
    post_notes=collections.defaultdict(list)
    for i in range(len(notes)):
        if i%4==0:
            post_notes['pitch'].append(notes['pitch'][i])
            post_notes['start'].append(notes['start'][i])
            post_notes['end'].append(notes['end'][i])
            post_notes['step'].append(notes['step'][i])
            post_notes['duration'].append(notes['duration'][i])
    return pd.DataFrame({name: np.array(value) for name, value in post_notes.items()})


#df = pd.DataFrame({"pitch":[0,1,2,3,4,5,6,7,8],
#                   "start":[0,1,2,3,4,5,6,7,8],
#                   "end":[0,1,2,3,4,5,6,7,8],"step":[0,1,2,3,4,5,6,7,8],"duration":[0,1,2,3,4,5,6,7,8]})
#print(detangle(df))
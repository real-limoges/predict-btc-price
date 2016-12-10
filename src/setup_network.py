from keras.models import Sequential

from keras.layers.recurrent import LSTM
from keras.layers.core import Dense, Activation, Dropout

import numpy as np
import random


def define_model(input_shape):
   
    #TODO Finish model
    model = Sequential()
    model.add
    model.add(LSTM(128, return_sequences=False, input_shape=input_shape))
    model.add(Dropout(0.2))
    model.add(LSTM(128, return_sequnces=False))
    model.add(Dropout(0.2))
    model.add(Dense(16))
    model.add(Activation(


    return model

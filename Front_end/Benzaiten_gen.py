
import numpy as np
import time
import pandas as pd
import sys
import os
import tensorflow as tf
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Dropout
from keras.layers import LSTM
from keras.utils import np_utils
from keras.callbacks import ModelCheckpoint

installedNN = []
filelst = []
for file in os.listdir():
  if file.endswith(".h5"):
    filelst.append(file)

nstringpass = ' '.join(filelst)
print(nstringpass)
nstringpass = nstringpass.replace("Benzaiten", "")
nstringpass = nstringpass.replace(".h5", "")
nstringpass = nstringpass.replace("\n", "")
print(nstringpass)
installedNN = list(nstringpass.split("  "))

print("installed Networks are ", installedNN)


utext = input("please type what you would like to generate, without qoutes.  ")
datafile = ('')

def Main(NetworkFile):

  textsource = datafile
  text=(open(textsource, 'r', encoding='utf-8').read())  #imports target text from a .txt file in the program local folder
  print("Loaded text source: ", textsource)
  text=text.lower()   #command for reducing all character to lowercase and text cleanup 

  characters = sorted(list(set(text)))   #sets up the target text with all unique charcters in the text being sorted in to a list

  n_to_char = {n:char for n, char in enumerate(characters)} #reads through the text and converts all the charcters into numbers

  char_to_n = {char:n for n, char in enumerate(characters)} #convert the numbers back in characters in the list 

  X = []  # training array

  Y = [] # target array

  setname = 'Benzaiten_'+textsource+'.h5'
  target = ""
  length = len(text) #get the charaacter lenght of the target text
  vocab = len(characters)
  print("Total characters: ", length)
  print("Total vocab: ", vocab)

  seq_length = 140 #the amount of characters that will be passed through at one time 

  for i in range(0, length-seq_length, 1): #itterates over the loaded sequence will make a note of all of the charcters and what is in front and behinde them. and write this to the training array and the target array
    squence = text[i:i + seq_length]
    label =text[i + seq_length]
    X.append([char_to_n[char] for char in squence])
    Y.append(char_to_n[label])
  n_patterns = len(X)
  print("total patterns: ", n_patterns)

  X_modified = np.reshape(X,  (n_patterns, seq_length, 1)) #reshapes the X array into a number that condenses the label information into a single number
  X_modified = X_modified / float(vocab) #makes this number a float that is less than 1 (0.something)
  Y_modified = np_utils.to_categorical(Y)  #makes the array a one hot, an array with nine zeros and one one, to remove and relationship from the orignial enumerated label 

  checkpiont_dir = './Training_checkpoints'
  checkpoint_prefix = os.path.join(checkpiont_dir, "Benzaiten_ckpt_{epoch}.h5")
  filepath = checkpoint_prefix

  def create_model():
    model = Sequential() #creates a models using a sequntial layering from Keras, meaning the model can be buildt by a layering commands
    model.add(LSTM(700, input_shape=(X_modified.shape[1], X_modified.shape[2]), return_sequences=True)) # first number is how many set from the for loop above will be fed run through in one go,after that is creating the right shape of variables 
    model.add(Dropout(0.2)) #used to remove data random data and reduce the chnace of the same data being procssed 
    model.add(LSTM(700)) # 
    model.add(Dropout(0.2))
    model.add(Dense(Y_modified.shape[1], activation='softmax'))
    checkpoint = ModelCheckpoint(filepath, monitor='loss', verbose=1, save_best_only=True, mode='min')
    callbacks_list = [checkpoint]
    return model

  NetworkFile = NetworkFile
  print(NetworkFile)

  def generate():
    model= create_model()
    model.load_weights('Benzaiten '+NetworkFile+'.h5')
    model.compile(loss='categorical_crossentropy', optimizer='adam')
    start = np.random.randint(0, len(X_modified)-1)
    pattern = X[start]
    print ("seed: ")
    olist=[]
    for i in range(9000):
      Xs = np.reshape(pattern, (1, len(pattern), 1))
      Xs = Xs / float(vocab)
      prediction = model.predict(Xs, verbose=0)
      index = np.argmax(prediction)
      result = n_to_char[index]
      seq_in = [n_to_char[value] for value in pattern]
      sys.stdout.write(result)
      pattern.append(index)
      pattern = pattern[1:len(pattern)]
      Cstring=""
      Cstring = pattern
      olist.append(Cstring)

    txt=""
    with open('OutputFile.txt', 'w') as f:
      for item in olist:
        f.write("%s\n" % item)
    print(txt)
  generate()


dataReplace = False

if utext in installedNN: 
  datafile = utext+'.txt'
  print('replaced input', datafile)
  dataReplace = True 
  time.sleep(1)
if dataReplace == True:
  print("--------------------------------strating generation-------------------------------")
  Main(utext)
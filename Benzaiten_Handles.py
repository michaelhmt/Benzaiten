import numpy as np
import pandas as pd
import sys
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Dropout
from keras.layers import LSTM
from keras.utils import np_utils

utext = input("Type 'generate' to generate text to output.txt or train, to train with current settings")

text=(open("MyImmortal.txt").read())  #imports target text from a .txt file in the program local folder
text=text.lower()   #command for reducing all character to lowercase and text cleanup 

characters = sorted(list(set(text)))   #sets up the target text with all charcter in the text being sorted in to a list

n_to_char = {n:char for n, char in enumerate(characters)} #reads through the text and converts all the charcters into numbers

char_to_n = {char:n for n, char in enumerate(characters)} #convert the numbers back in characters in the list 

X = []  # training array

Y = [] # target array

length = len(text) #get the charaacter lenght of the target text

seq_length = 100 #the amount of characters that will be passed through at one time 
def Train():
	for i in range(0, length-seq_length, 1): #itterates over the loaded sequence will make a note of all of the charcters and what is in front and behinde them. and write this to the training array and the target array
		squence = text[i:i + seq_length]
		label =text[i + seq_length]
		X.append([char_to_n[char] for char in squence])
		Y.append(char_to_n[label])

	X_modified = np.reshape(X,  (len(X), seq_length, 1)) #reshapes the X array into a number that condenses the label information into a single number
	X_modified = X_modified / float(len(characters)) #makes this number a float that is less than 1 (0.something)
	Y_modified = np_utils.to_categorical(Y)  #makes the array a one hot, an array with nine zeros and one one, to remove and relationship from the orignial enumerated label 

	model = Sequential() #creates a models using a sequntial layering from Keras, meaning the model can be buildt by a layering commands
	model.add(LSTM(400, input_shape=(X_modified.shape[1], X_modified.shape[2]), return_sequences=True)) # first number is how many set from the for loop above will be fed run through in one go,after that is creating the right shape of variables 
	model.add(Dropout(0.2)) #used to remove data random data and reduce the chnace of the same data being procssed 
	model.add(LSTM(400)) # 
	model.add(Dropout(0.2))
	model.add(Dense(Y_modified.shape[1], activation='softmax'))
	model.compile(loss='categorical_crossentropy', optimizer='adam')

	model.fit(X_modified, Y_modified, epochs=110, batch_size=60)

	model.save_weights('Benzaiten_400_0.2_700_0.2_100_E110.h5')
	model.load_weights('Benzaiten_400_0.2_700_0.2_100-E110.h5')
	string_mapped = X[1200] #last row from X that is 99 characters long 
	full_string = [n_to_char[value] for value in string_mapped]
	#-----generating characters------
	olist=[]
	for i in range(seq_length):
		x = np.reshape(string_mapped,(1,len(string_mapped), 1))   #sets up a local veriable that makes the incoming data readable text
		x = x / float(len(characters))
		pred_index = np.argmax(model.predict(x, verbose=0))   # takes the above modeland uses it to geuss the next charcter
		seq = [n_to_char[value] for value in string_mapped] # used to predict the most likley chracter
		full_string.append(n_to_char[pred_index])
		string_mapped.append(pred_index)    
		string_mapped = string_mapped[1:len(string_mapped)]
		Cstring=""
		for char in full_string:
			Cstring = Cstring+char
		olist.append(Cstring)


	#-----combing text------
	txt=""
	for char in full_string:
		txt = txt+char
	print(txt)
	with open('OutputFile.txt', 'w') as f:
		for item in olist:
			f.write("%s\n" % item)

def Gentext():
	model.load_weights('Benzaiten_ActiveSet.h5')

	string_mapped = X[1200] #last row from X that is 99 characters long 
	full_string = [n_to_char[value] for value in string_mapped]
	#-----generating characters------
	olist=[]
	for i in range(seq_length):
		x = np.reshape(string_mapped,(1,len(string_mapped), 1))   #sets up a local veriable that makes the incoming data readable text
		x = x / float(len(characters))
		pred_index = np.argmax(model.predict(x, verbose=0))   # takes the above modeland uses it to geuss the next charcter
		seq = [n_to_char[value] for value in string_mapped] # used to predict the most likley chracter
		full_string.append(n_to_char[pred_index])
		string_mapped.append(pred_index)    
		string_mapped = string_mapped[1:len(string_mapped)]
		Cstring=""
		for char in full_string:
			Cstring = Cstring+char
		olist.append(Cstring)


	#-----combing text------
	txt=""
	for char in full_string:
		txt = txt+char
	print(txt)
	with open('OutputFile.txt', 'w') as f:
		for item in olist:
			f.write("%s\n" % item)

train()
'''print(sys.argv)
if utext == "generate": 
	Gentext()
if utext == "train":
	Train()'''




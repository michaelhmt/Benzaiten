import os
import re
#dir = os.listdir()
#dirlst = [dir]
#dirstring = ' '.join([str(item) for item in dirlst])

#print(dirstring)
installedNN = []
filelst = []
for file in os.listdir():
	if file.endswith(".h5"):
		filelst.append(file)
#print(installedNN)

nstringpass = ' '.join(filelst)
print(nstringpass)
nstringpass = nstringpass.replace("Benzaiten", "")
nstringpass = nstringpass.replace(".h5", "")
print(nstringpass)
installedNN = list(nstringpass.split("  "))


#print(installedNN)
#junk = len(installedNN)
#junk = junk -1
#del installedNN[junk]
#stingpass = ''.join(installedNN)
#installedNN = []
#installedNN = list(stingpass.split(" "))
print(installedNN)

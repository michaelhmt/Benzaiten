L1 = []



po="ONEONEONE"
L1.append(po)
ZO="NONONONO"
L1.append(ZO)
In="ADDADDADD"
L1.append(In)

print(L1)

with open('OutputFile.txt', 'w') as f:
	for item in L1:
		f.write("%s\n" % item)

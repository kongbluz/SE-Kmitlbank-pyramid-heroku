import random
import string

def GETOTP():
	s = ""
	c = random.randint(1,6)
	cu = int (c/2)
	for i in range(0, cu):
		x = random.choice(string.ascii_letters)
		x2 = random.choice(string.digits)
		x3 = random.randint(1,2)
		if x3==1:
			s+=str(x)
			s+=str(x2)
		else:
			s+=str(x2)
			s+=str(x)
	c2 = random.randint(1,2)
	if c2==1:
		for i2 in range(0,6-(cu*2)):
			y = random.choice(string.ascii_letters)
			s+=str(y)
	else:
		for i2 in range(0,6-(cu*2)):
			y2 = random.choice(string.digits)
			s+=str(y2)

	return s

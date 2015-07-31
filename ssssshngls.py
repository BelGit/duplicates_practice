import nltk
import string
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
import binascii

tokenizer = RegexpTokenizer('\w+|\$[\d\.]+|\S+')
stop_words = stopwords.words('russian')

path = 'C:\Anaconda/test.txt'
fid = open(path,'r')
lines1 = fid.readlines()
fid.close()

path = 'C:\Anaconda/test1.txt'
fid = open(path,'r')
lines2 = fid.readlines()
fid.close()

def canonize(text):
	tokens = []

	lines = map(tokenizer.tokenize, [line.decode('utf-8').strip() for line in text])
	for line in lines:
		for token in line:
			if not token in string.punctuation:
				token.strip(string.punctuation)
				if not token in stop_words:
					tokens.append(token.lower())
	return tokens

def shingle(tokens):
	shingLen = 10
	res = []
	for i in range(len(tokens)-(shingLen-1)):
		res.append (binascii.crc32(' '.join( [x for x in tokens[i:i+shingLen]] ).encode('utf-8')))
	return res

def compaire(source1, source2):
	same = 0
	for i in range(len(source1)):
		if source1[i] in source2:
			same = same + 1
	return float(same*2)/float(len(source1) + len(source2))*100

print compaire(shingle(canonize(lines1)), shingle(canonize(lines2)))
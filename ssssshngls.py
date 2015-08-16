import nltk
import string
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
import binascii
import gensim
from gensim import corpora, models, similarities
import pymorphy2
import sys

path = sys.path[0] + '\\test_docs'

path1 = path + '\\doc0.txt'
fid = open(path1,'r')
lines1 = fid.readlines()
fid.close()

path2 = path + '\\doc1.txt'
fid = open(path2,'r')
lines2 = fid.readlines()
fid.close()



morph = pymorphy2.MorphAnalyzer()
tokenizer = RegexpTokenizer('\w+|\$[\d\.]+|\S+')
stop_words = stopwords.words('russian')

def normalize(token):
	try: 
		gram_info = morph.parse(token)
		return gram_info[0].normal_form
	except:
		return token

def canonize(text):
	tokens = []

	lines = map(tokenizer.tokenize, [line.decode('utf-8').strip() for line in text])
	for line in lines:
		for token in line:
			if not token in string.punctuation:
				token.strip(string.punctuation)
				if not token in stop_words:
					tokens.append(normalize(token.lower()))
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
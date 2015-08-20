import nltk
import string
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
import binascii
import gensim
from gensim import corpora, models, similarities
import sys

path = sys.path[0] + '\\test_docs'

path1 = path + '\\corpus_sample.vert'
fid = open(path1,'r')
lines = fid.readlines()
fid.close()

stop_words = stopwords.words('russian')

ids = []
docs = []

def canonize(line):
	tokens = []
	tokens = line.split()
	token = tokens[-1]
	if not '-' in tokens[-1]:
		token = tokens[-2]
	return token.split('-')[0]

def shingle(tokens):
	shingLen = 10
	res = []
	for i in range(len(tokens)-(shingLen-1)):
		res.append (binascii.crc32(' '.join( [x for x in tokens[i:i+shingLen]])))
	return res

def compaire(source1, source2):
	same = 0
	for i in range(len(source1)):
		if source1[i] in source2:
			same = same + 1
	return float(same*2)/float(len(source1) + len(source2))*100



i = 0
while i < len(lines):
	if "doc" in lines[i]:
		tokens = []
		ids.append(lines[i].split()[1].split('=')[1].strip('"'))
		i+=1
		while not "doc" in lines[i]:
			if not "<" in lines[i]:
				token = canonize(lines[i])
				if not token in string.punctuation:
					if not token in stop_words:
						tokens.append(token.lower())
			i+=1
		docs.append(tokens)
	i+=1

for i in range(len(docs) - 1):
	for j in range(i + 1, len(docs)):
		percent = compaire(shingle(docs[i]), shingle(docs[j]))
		if percent > 0:
			print ids[i] + " and " + ids[j]
			print percent

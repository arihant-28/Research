# encoding=utf8  
import sys  

reload(sys)  
sys.setdefaultencoding('utf8')

import cPickle as pickle
from numpy import matrix
from numpy import array
import sys
import codecs
import gensim
from gensim.models import Word2Vec,word2vec

UTF8Writer = codecs.getwriter('utf8')
sys.stdout = UTF8Writer(sys.stdout)

print "loading models"
#emodel2 = word2vec.Word2Vec.load('model4')
#emodel3 = word2vec.Word2Vec.load('model3')
#emodel1 = word2vec.Word2Vec.load('model2')
emodel1 = word2vec.Word2Vec.load('model1')

count  = 1
print "loading vocab"
efreq = pickle.load(open("frequency_dict_model1","rb"))

f = open("rw.txt",'r')  # evaluation words
r=f.readlines()
f.close()
relevent={}
for i in r:
	l1 = map(str,i.split())
	relevent[l1[0]]=True
	relevent[l1[1]]=True

print len(relevent)
new_model = {}
for i in emodel1.vocab:
	#if i in relevent:
	if True:
		new_model[i] = list(emodel1[i])



def construct_matrix(lis,model1,model2):
	B,C=[],[]
	for i in lis:
		tmp1,tmp2=[],[]
		for j in xrange(len(model1[i])):
			tmp1.append(model2[i][j])
			tmp2.append(model1[i][j])
		B.append(tmp1)
		C.append(tmp2)
	B=matrix(B)
	C=matrix(C)
	X = (B.I)*C
	return X



def transformers(x,X,model2):
	start = model2[x]
	start = matrix(start)
	end = start*X
	end = end.tolist()[0]
	end = array( end )
	return end


def daal_do(model1,model2):

	for_matrix = []
	for j in efreq:
		i = unicode(j)
		if efreq[j] > 1000 and i in model1.vocab and i in model2.vocab:
			for_matrix.append(i)

	print len(for_matrix),"reliable words found for training transformation"	
	if len(for_matrix) < 500:
		print "merge failed"
		return
	X = construct_matrix(for_matrix,model1,model2)

	words_to_import = {}
	for i in model2.vocab:
		if i not in model1.vocab and i not in new_model:
			words_to_import[i]=True

	for i in words_to_import:
		j = str(i)
		if len(j)>2 and j[-2::]=="\'s":
		#if True:
			new_model[i] = transformers(i,X,model2)
	print len(words_to_import),"words merged"


if count == 1:
	pass
else:

	if count > 1:
		daal_do(emodel1,emodel2)
	if count > 2:
		daal_do(emodel1,emodel3)
	if count  > 3:
		daal_do(emodel1,emodel4)

f = open("model.txt",'w')

f.write(str(len(new_model))+" 300\n")
#print len(new_model),300

for i in new_model:
	#if i not in relevent:
	#	continue
	f.write(i.decode('utf-8')+" ")
	#print i.decode('utf-8'),
	for j in new_model[i]:
		#print j,
		f.write(str(j)+" ")
	#print
	f.write("\n")

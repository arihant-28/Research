from sys import stdin
import random
from scipy import stats
import gensim
from gensim.models import Word2Vec,word2vec
from numpy import array
from numpy import matrix
import numpy as np
import codecs
import sys
import cPickle as pickle
UTF8Writer = codecs.getwriter('utf8')
sys.stdout = UTF8Writer(sys.stdout)
fmodel = word2vec.Word2Vec.load('model1')
emodel = word2vec.Word2Vec.load('model2')
ffreq = pickle.load(open("freq_dict","rb"))
efreq = pickle.load(open("freq_dict","rb"))
X = pickle.load(open("../transformation_matrix.p","rb"))


sz = 300
print len(fmodel.vocab)
def normalised_dot_product(a,b):
  s = dot_product(a,b)
  x,y = 0.0,0.0
  for i in xrange(len(a)):
    x+=a[i]*a[i]
  for i in xrange(len(b)):
    y+=b[i]*b[i]
  x = pow(x,0.5)
  y = pow(y,0.5)
  if s ==0.0:
    return 0.0
  return s/(x*y)

def dot_product(a,b):
    s=0
    for i in xrange(len(a)):
        s+=a[i]*b[i]
    return s


def transformers(x):
	start = emodel[x]
	start = matrix(start)
	end = start*X
	end = end.tolist()[0]
	end = array( end )
	return end

def need_to_transform(x,y):
	#if x in fmodel and x in ffreq and ffreq[x]>=500:
	#	return False
	#if y not in emodel or y not in efreq or efreq[y]<50:
	#	return False
	return True

def handle_word(x,y):
	
	if need_to_transform(x,y):
		v1=transformers(y)
		return v1

	v1 = []
	if x not in fmodel:
	  	v1 = [0 for j in xrange(sz)]
	else:
		v1 = fmodel[x]
	return v1

l1 = []
l2 = []
for i in stdin:
 
  l = map(str,i.split())
  a = l[0]
  b = l[1]
  c = l[2]
  
  c = float(c)
  v1,v2 = [],[]

  y = l[3]
  z = l[4]
  if len(l)>6:
    y = l[6]
    z = l[7]
  v1 = handle_word(a,y)
  v2 = handle_word(b,z)
  
  l1.append(c)
  l2.append(normalised_dot_product(v1,v2)*10)

print stats.spearmanr(l1,l2)



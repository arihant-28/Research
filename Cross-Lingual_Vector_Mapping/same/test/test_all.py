from sys import stdin
import random
from scipy import stats
import gensim
from gensim.models import Word2Vec,word2vec
import codecs
import sys
import cPickle as pickle
UTF8Writer = codecs.getwriter('utf8')
sys.stdout = UTF8Writer(sys.stdout)
#model = word2vec.Word2Vec.load('../TRAINING/1000full4m2_w2v.txt')
#model = word2vec.Word2Vec.load_word2vec_format('../avengers.txt')
#model = word2vec.Word2Vec.load_word2vec_format('../madam/conceptnet-numberbatch-201609_en_main.txt')
#model = word2vec.Word2Vec.load_word2vec_format('../mkmkc/small_big_model.txt')
#model = word2vec.Word2Vec.load('../TRAINING/1000full2m2_w2v.txt')
#model = word2vec.Word2Vec.load_word2vec_format('../GoogleNews-vectors-negative300.bin',binary =True) 
#model = word2vec.Word2Vec.load('../v7//e_model/west300_w2v.txt')
model = word2vec.Word2Vec.load('../aakhri/train/smallWest_w2v.txt')
#model = word2vec.Word2Vec.load('../mkmkc/krazynet.txt')
sz = 300
#efreq = pickle.load(open("../v7/efreq/bizfreq.p","rb"))

print len(model.vocab)
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

def handle_word(x):
	v = []
	if x not in model:
	  	v = [0 for j in xrange(sz)]
	else:
		v = model[x]
	return v
cou = 0
l1 = []
l2 = []
s = set()
print len(model.vocab) 
f = open('WS.csv', 'r')
r = f.readlines()

for i in r:   
  # for rw.txt and rg.txt
  #l = map(str,i.split(':'))
  #a = l[0]
  #b = l[1]
  #c = l[2]
  ##
  
  # for WS.csv
  a,b,c = map(str,i.split(','))
  ##
  c = float(c)
  v1,v2 = [],[]

  v1 = handle_word(a)
  v2 = handle_word(b)
  flag = 0
  if sum(v1)==0:
    s.add(a)
    flag = 1
  if sum(v2)==0:
    s.add(b)
    flag= 1
  if flag == 1:
    cou+=1
  
 
  l1.append(c)
  l2.append(normalised_dot_product(v1,v2)*10)

print "ws"
print len(s)
print cou
print stats.spearmanr(l1,l2)
f.close()


f = open('rg.txt', 'r')
r = f.readlines()

cou = 0
l1 = []
l2 = []
s = set()
for i in r:
   
  # for rw.txt and rg.txt
  l = map(str,i.split())
  a = l[0]
  b = l[1]
  c = l[2]
  ##
  
  '''
  # for WS.csv
  #a,b,c = map(str,i.split(','))
  ##
  '''
  c = float(c)
  v1,v2 = [],[]

  v1 = handle_word(a)
  v2 = handle_word(b)
  flag = 0
  if sum(v1)==0:
    s.add(a)
    flag = 1
  if sum(v2)==0:
    s.add(b)
    flag= 1
  if flag == 1:
    cou+=1
  
  l1.append(c)
  l2.append(normalised_dot_product(v1,v2)*10)

print  "rg"
print len(s)
print cou
print stats.spearmanr(l1,l2)
f.close()


f = open('rw.txt', 'r')
r = f.readlines()
cou = 0
l1 = []
l2 = []
s = set()
gg =0 
for i in r:
   
  # for rw.txt and rg.txt
  l = map(str,i.split())
  a = l[0]
  b = l[1]
  c = l[2]
  ##
  
  '''
  # for WS.csv
  #a,b,c = map(str,i.split(','))
  ##
  '''
  c = float(c)
  v1,v2 = [],[]

  v1 = handle_word(a)
  v2 = handle_word(b)
  flag = 0
  if sum(v1)==0:
    s.add(a)
    flag = 1
  if sum(v2)==0:
    s.add(b)
    flag= 1
  if flag == 1:
    cou+=1
  
  l1.append(c)
  l2.append(normalised_dot_product(v1,v2)*10)
print "rw"
print len(s)
unseen = list(s)
unseen = sorted(unseen)
print unseen
print stats.spearmanr(l1,l2)
f.close()

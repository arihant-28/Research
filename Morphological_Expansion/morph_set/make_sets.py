from sys import stdin
dic = {}
import random
from scipy import stats
import gensim
from gensim.models import Word2Vec,word2vec
import codecs
import sys
UTF8Writer = codecs.getwriter('utf8')
sys.stdout = UTF8Writer(sys.stdout)
import cPickle as pickle
model = word2vec.Word2Vec.load('model_path')
word_freq = pickle.load(open("freq_dict_path","rb"))

prefixtransitions  = pickle.load(open('../TRIE/prefixtransitions.p'))
transitions  = pickle.load(open('../TRIE/transitions.p'))

sim = 0.15

print "model loaded"

trans = {}
for i in prefixtransitions:
   trans[(i,True)] = prefixtransitions[i]
for i in transitions:
   trans[(i,False)] = transitions[i]

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

def pair_similarity(a,b):
	x,y = a[0],a[1]
	p,q = b[0],b[1]
	d1,d2 = [],[]
	for i in xrange(len(x)):
		d1.append(x[i]-y[i])
		d2.append(p[i]-q[i])
	return normalised_dot_product(d1,d2)

def dot_product(a,b):
    s=0
    for i in xrange(len(a)):
        s+=a[i]*b[i]
    return s

def ends_with(x,to_del):
    if len(x) > len(to_del):
        if x[len(x) -len(to_del)::] == to_del:
            return True
    return False

def starts_with(x,to_begin):
    if len(x) > len(to_begin):
        if x[0:len(to_begin)] == to_begin:
            return True
    return False

def new_word_prefix(x,i):
    to_add = ""
    to_del = ""
    word = ""
    
    k = i

    i=(i[0][::-1],i[1][::-1])    
    j = 0
    for j in xrange(len(i[0])):
        if j>= len(i[1]):
            break
        if i[0][j]!=i[1][j]:
            j-=1
            break

    if j < len(i[0]):
        to_del = i[0][j::]
    if j < len(i[1]):
        to_add = i[1][j::]
    to_del = to_del[::-1]
    to_add = to_add[::-1]

    if len(to_add)>0 and len(to_del)>0 and to_add[-1]==to_del[-1]:
      to_add = to_add[0:len(to_add)-1]
      to_del = to_del[0:len(to_del)-1]


    change = "B_"+to_del+"_"+to_add

    if starts_with(x,to_del):
        word = to_add
        word += x[len(to_del)::]
    return (word,change)


def new_word(x,i,p):
    if p==True:
        return new_word_prefix(x,i)
    to_add = ""
    to_del = ""
    word = ""
    
    j =0
    for j in xrange(len(i[0])):
        if j>= len(i[1]):
            break
        if i[0][j]!=i[1][j]:
            break
    if j < len(i[0]):
        to_del = i[0][j::]
    if j < len(i[1]):
        to_add = i[1][j::]

    if len(to_add)>0 and len(to_del)>0 and to_add[0]==to_del[0]:
      to_add = to_add[1::]
      to_del = to_del[1::]
   
 
    
    change = "A_"+to_del+"_"+to_add

    if ends_with(x,to_del):
        word = x[0:len(x)-len(to_del)]
        word += to_add
    return (word,change)



def soft_set(x,mor):
	if x.encode("utf8") not in model:
		return
	if len(x)<= 3:
		return
	word = ""
	for i in trans:
		tmp = new_word(x,i[0],i[1])
		word = tmp[0]
		change = tmp[1]
		if word == "" or len(word)<4:
			continue	
	
		if word.encode("utf8") in model and word in word_freq and normalised_dot_product(model[x.encode("utf8")],model[word.encode("utf8")])>sim:
			mor.add((word,change))
morphs = {}

def validate_set(lis):
	if len(lis)<2:
		return True
	if len(lis)>=30:
		return False
	lis = list(lis)
	x = lis[0]
	for i in lis:
		if normalised_dot_product(model[x[0].encode("utf8")],model[i[0].encode("utf8")]) < sim:
			return False
	return True


def get_set(x):
  mor = set()
  soft_set(x,mor)
  if validate_set(mor) == True:
    morphs[x] = list(mor)

for i in word_freq:
  if word_freq[i]>=100 and len(i)>2:
    get_set(i)

pickle.dump( morphs, open( "small_sets.p", "wb" ) )



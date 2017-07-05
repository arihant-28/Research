import cPickle as pickle
from numpy import matrix
import sys
import codecs
import gensim
from gensim.models import Word2Vec,word2vec

UTF8Writer = codecs.getwriter('utf8')
sys.stdout = UTF8Writer(sys.stdout)

print "loading english model"
emodel = word2vec.Word2Vec.load_word2vec_format('model2')
print "loading second language model"
fmodel = word2vec.Word2Vec.load('model1')

print "loading english vocab"
efreq = pickle.load(open("freq_dict","rb"))
print "loading second language vocab"
ffreq = pickle.load(open("freq_dict","rb"))

print "loading parallel data"
f1 = open("parallel_data",'r')
r1 = f1.readlines()
f1.close()
l1 = []
for i in r1:
	l1.append(map(str,i.split('|||')))

print "loading fast_align output"
f2 = open("fast_align_output",'r')
r2 = f2.readlines()
f2.close()

l2 = []
for i in r2:
	l2.append(map(str,i.split()))


print "generating many-1 alignment"
dic = {}
cid = {}
mdic = {}
cdic = {}
for i in xrange(len(l1)):
	en = l1[i][0].strip()
	fr = l1[i][1].strip()
	e = map(str,en.split())
	f = map(str,fr.split())
	m = []
	for j in l2[i]:
		tmp = map(int,j.split('-'))
		m.append(tmp)
	for j in m:

		if e[j[0]] not in dic:
			dic[e[j[0]]] = [ [f[j[1]],1] ]
			mdic[e[j[0]]] = 1
			cid[(e[j[0]],f[j[1]])] = 0
			cdic[e[j[0]]] = [f[j[1]],1]
		else:
			if (e[j[0]],f[j[1]]) not in cid:
				dic[e[j[0]]].append([f[j[1]],1])
				cid[(e[j[0]],f[j[1]])]=len(dic[e[j[0]]])-1
			else:
				dic[e[j[0]]][cid[(e[j[0]],f[j[1]])]][1]+=1
			mdic[e[j[0]]]+=1
			if dic[e[j[0]]][cid[(e[j[0]],f[j[1]])]][1] > cdic[e[j[0]]][1]:
				cdic[e[j[0]]] = dic[e[j[0]]][cid[(e[j[0]],f[j[1]])]]


print "generating 1-1 alignment"
final_list = []
for i in cdic:
	final_list.append([cdic[i][1],mdic[i],i,cdic[i][0]])

final_list = sorted(final_list,reverse=True)

for_matrix = []

ddic = {}

for i in final_list:
	if i[2] in emodel and i[2] in efreq and efreq[i[2]]>=500:
		pass
	else:
		continue
	if i[3] in fmodel and i[3] in ffreq and ffreq[i[3]]>=500:
		pass
	else:
		continue

	if i[0] > 25 and i[0]*1.0/i[1] >= 0.5 and i[3] not in ddic:
		for_matrix.append([i[2],i[3]])
		#print i[0],i[1],i[2].decode('utf-8'),i[3].decode('utf-8')
		#ddic[i[3]]=True	



def construct_matrix(lis):
	B,C=[],[]
	for i in lis:
		tmp1,tmp2=[],[]
		for j in xrange(len(emodel[i[0]])):
			tmp1.append(emodel[i[0]][j])
			tmp2.append(fmodel[i[1]][j])
		B.append(tmp1)
		C.append(tmp2)
	B=matrix(B)
	C=matrix(C)
	X = (B.I)*C
	return X

print "constructing matrix"
biggie = construct_matrix(for_matrix)
pickle.dump( biggie, open( "transformation_matrix.p", "wb" ) )



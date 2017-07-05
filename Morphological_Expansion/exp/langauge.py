import sys
from scipy import stats
import codecs
import cPickle as pickle
import random
UTF8Writer = codecs.getwriter('utf8')
sys.stdout = UTF8Writer(sys.stdout)
sys.setrecursionlimit(10000)
morphs = pickle.load(open("../morph_set/small_sets.p","rb"))


done = set()

def generate_it(lis,st,ind):
	if ind>=len(lis):
		#if len(st.split())>len(lis):
		if True:
			done.add(st)
		return

	flag = 0
	r = 0

	if lis[ind] in  morphs and len(morphs[lis[ind]])>0:

		flag = 1

		r = random.randint(0, 2*( len(morphs[lis[ind]])-1) )
		
		if r <= len(morphs[lis[ind]])-1:

			flag = 2
			i = morphs[lis[ind]][r]

			tmp_st = st
			#tmp_st +=" "+i[0]+" "+i[1]
			tmp_st += " "+i[0]
			generate_it(lis,tmp_st,ind+1)

	else:
		tmp_st = st
		tmp_st+= " "+lis[ind]
		generate_it(lis,tmp_st,ind+1)
	
	
	if flag == 1:
		tmp_st = st
		tmp_st+= " "+lis[ind]
		generate_it(lis,tmp_st,ind+1)
		


for i in sys.stdin:
	
	l2 = map(str,i.split())
	flag = 0
	l = []
	for j in l2:
		try:
    			l.append( j.decode('utf-8') )
  		except:
    			flag = 1
	#if flag == 1:
	#	continue
	done.clear()

	orig = ""
	for j in l:
		orig+= " "+j

	done.add(orig)	


	for j in xrange(1):
		generate_it(l,"",0)
	for j in done:
		print j




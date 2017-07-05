#!/usr/bin/python
# -*- coding: utf-8 -*-

import codecs
import sys
import cPickle as pickle
from gensim.models import Word2Vec,word2vec

UTF8Writer = codecs.getwriter('utf8')
sys.stdout = UTF8Writer(sys.stdout)

model = word2vec.Word2Vec.load('model_path')
word_freq = pickle.load(open("freq_dict_path","rb"))
morphenes = pickle.load(open("../TRIE/all_morphenes.p","rb"))
print "model loaded"
transitions = {}
thres = 100
sim = 0.2


def normalised_dot_product(a,b):
  s = dot_product(a,b)
  x,y = 0.0,0.0
  for i in xrange(len(a)):
    x+=a[i]*a[i]
  for i in xrange(len(b)):
    y+=b[i]*b[i]
  x = pow(x,0.5)
  y = pow(y,0.5)
  return s/(x*y)


def dot_product(a,b):
  s = 0
  for i in xrange(len(a)):
    s+= a[i]*b[i]
  return s

def dot_product_pair(a,b):
  a=(a[0].encode("utf8"),a[1].encode("utf8"))
  b=(b[0].encode("utf8"),b[1].encode("utf8"))
  x = []
  for i in xrange(len(model[a[0]])):
    x.append(model[a[0]][i]-model[a[1]][i])
  y = []
  for i in xrange(len(x)):
    y.append(x[i]+model[b[1]][i])

  return normalised_dot_product(model[b[0]],y)

def add_transition(i,cou):
  if tuple(i) in transitions:
    transitions[tuple(i)] = max(cou,transitions[tuple(i)])
  else:
    transitions[tuple(i)] = cou
  if tuple(i[::-1]) in transitions:
    transitions[tuple(i[::-1])] = max(cou,transitions[tuple(i[::-1])])
  else:
    transitions[tuple(i[::-1])] = cou


def extract_transitions_paper(group):
  ma = 0
  if len(group) < 11:
    return
  ma_group = group[0]
  for i in group:
    cou = 0
    for j in group:
      if dot_product_pair(i,j) > sim:
        cou+=1
    if cou >=11:
      if cou > ma:
        ma = cou
        ma_group = i

  if ma >=11:
    i = ma_group
    print i[0],i[1]
    add_transition(i,ma)


    tmp = {}
    for j in group:
      if dot_product_pair(i,j) > sim:
        tmp[tuple(j)] = 1
    tmp_group = []

    for l in group:
      if tuple(l) not in tmp:
        tmp_group.append(l)
    extract_transitions_paper(tmp_group)
  return


def ch(x):
	ma,mi="",""
	if len(x[0])>len(x[1]):
		ma = x[0]
		mi = x[1]
	else:
		ma = x[1]
		mi = x[0]
	if ma[0:len(mi)]==mi:
		return False
	else:
		return True

def x_y(x,y):
  if ch((x,y))==False:
    return
  common = set(morphenes[x]).intersection(morphenes[y])
  if len(common) < 11:
    return
  group = []
  for i in common:
    j = i+x
    k = i+y
    if j in word_freq and word_freq[j]>thres and k in word_freq and word_freq[k]>thres and j.encode("utf8") in model and k.encode("utf8") in model:
      group.append([j,k])
      if len(group) > 1000:
        extract_transitions_paper(group)
        group = []
  extract_transitions_paper(group)
  return

def null_x(x):
  global word_freq 
  group = []
  for i in morphenes[x]:
    j = i+x

    if j in word_freq and word_freq[j]>thres and i in word_freq and word_freq[i]>thres and i.encode("utf8") in model and j.encode("utf8") in model:
      group.append([i,j])
      if len(group) > 1000:
        extract_transitions_paper(group)
        group = []
  extract_transitions_paper(group)
  return

if __name__ == "__main__":

  c = 0
  completed_i = set()
  

  for i in morphenes:
    if len(morphenes[i])<10:
      continue
    null_x(i)
    c+=1
    if len(morphenes[i]) < thres*5:
      continue
    for j in morphenes:
      if len(morphenes[j]) <thres*5:
        continue
      if j in completed_i:
        continue
      x_y(i,j)
    completed_i.add(i)
  

  pickle.dump( transitions, open( "papertransitions.p", "wb" ) )     # merged all the morphenes
  for i in transitions:
    print i[0],i[1]

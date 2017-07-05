#!/usr/bin/python
# -*- coding: utf-8 -*-

import codecs
import sys
import cPickle as pickle
from gensim.models import Word2Vec,word2vec

UTF8Writer = codecs.getwriter('utf8')
sys.stdout = UTF8Writer(sys.stdout)

model = word2vec.Word2Vec.load('model_path')
word_freq = pickle.load(open("frequency_dict_path","rb"))
morphenes = pickle.load(open("../TRIE/all_prefixmorphenes.p","rb"))
print "model loaded"
transitions = {}
thres =100
sim = 0.15



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
  if len(group) < 10:
    return
  ma_group = group[0]
  for i in group:
    cou = 0
    for j in group:
      if dot_product_pair(i,j) > sim:
        cou+=1
    if cou >=10:
      if cou > ma:
        ma = cou
        ma_group = i

  if ma >=10:
    i = ma_group
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


def x_y(x,y):
  if len(morphenes[x])<2:
    return

  group = []
  for i in morphenes[x]:
    j = x[::-1]+i[::-1]
    if j in word_freq and word_freq[j]>thres and i[::-1] in word_freq and word_freq[i[::-1]]>thres and i[::-1].encode("utf8") in model and j.encode("utf8") in model:
      group.append([i[::-1],j])
      if len(group)>1000:
        extract_transitions_paper(group)
        group = []
        return
 
  extract_transitions_paper(group)
  return


def null_x(x):

  if len(morphenes[x])<2:
    return
  group = []
  for i in morphenes[x]:
    j = x[::-1]+i[::-1]
    if j in word_freq and word_freq[j]>thres and i[::-1] in word_freq and word_freq[i[::-1]]>thres and i[::-1].encode("utf8") in model and j.encode("utf8") in model:
      group.append([i[::-1],j])
      if len(group)>1000:
        extract_transitions_paper(group)
        group = []
 
  extract_transitions_paper(group)
  return

if __name__ == "__main__":

  completed_i = set()
  for i in morphenes:
    null_x(i)
    if len(morphenes[i])<thres*5:
      continue
    for j in morphenes:
      if len(morphenes[j])<thres*5:
        continue
      if j in completed_i:
        continue
    x_y(i,j)
    completed_i.add(i)

  pickle.dump( transitions, open( "paperprefixtransitions.p", "wb" ) )     # merged all the morphenes
  for i in transitions:
    print i[0],i[1]

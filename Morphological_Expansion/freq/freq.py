#!/usr/bin/python
# -*- coding: utf-8 -*-
import cPickle as pickle
import codecs
import sys
UTF8Writer = codecs.getwriter('utf8')
sys.stdout = UTF8Writer(sys.stdout)

from sys import stdin
freq = {}
for i in stdin:
  l = map(str,i.split())
  for j in l:
    j = unicode(j,'utf-8')
    if j in freq:
      freq[j]+=1
    else:
      freq[j]=1

for i in freq:
  if freq[i]>100:
    print i,freq[i]

pickle.dump( freq, open( "freq.p", "wb" ) )  

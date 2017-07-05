#!/usr/bin/python
# -*- coding: utf-8 -*-


import sys
#sys.setrecursionlimit(100000)

import codecs
import cPickle as pickle

UTF8Writer = codecs.getwriter('utf8')
sys.stdout = UTF8Writer(sys.stdout)
from sys import stdin

suffixes = {}
morphenes = {}


def make_unicode(inp):
    if type(inp) != unicode:
        inp = inp.decode('utf-8')
        return inp
    else:
        return inp

class Node:
    def __init__(self,c):
        self.c = c
        self.next = {}
        self.cnt = 0
        self.ends = 0


def insert(node, word):
    word = word[::-1]
    for w in word:
        if w not in node.next:
            node.next[w] = Node(w)
        node = node.next[w]
        node.cnt += 1
    node.ends += 1

def find_morphenes(node, path, threshold):
    if len(node.next) >= threshold and len(path)>0:
        morphenes[path[::-1]] = []
    for w in node.next:
        find_morphenes(node.next[w], path+w, threshold)

def find_words(node, path):
    if node.ends != 0:
        tmp = ""
        for i in path:
            tmp += i
            current_morphene = tmp[::-1]
            if current_morphene in morphenes:
                morphenes[current_morphene].append( path[ len( current_morphene ):: ] [::-1] )

    for w in node.next:
        find_words(node.next[w], path+w)


root = Node( u"$" )

for i in stdin:
    words=map(str,i.split())
    for word in words:
      try:
        insert(root, word.decode('utf-8'))
        #insert(root, unicode(word,"utf-8"))
      except:
        nfg = 0

print "trie constructed"

find_morphenes(root, "",10)
find_words(root , "")


# for small files


for i in morphenes:
	if len(morphenes[i])<1000:
 		continue
	print i
	for j in morphenes[i]:
		print j,
	print
		

for i in morphenes:
	print i
	for j in morphenes[i]:
		print j,
	print j
pickle.dump( morphenes, open( "all_morphenes.p", "wb" ) )     # suffix and its set

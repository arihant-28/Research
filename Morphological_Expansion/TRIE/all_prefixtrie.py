#!/usr/bin/python
# -*- coding: utf-8 -*-

import codecs
import sys
import cPickle as pickle

UTF8Writer = codecs.getwriter('utf8')
sys.stdout = UTF8Writer(sys.stdout)

suffixes = {}
morphenes = {}

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

for i in sys.stdin:
    words=map(str,i.split())
    for word in words:
      tmp = word.decode('utf-8')
      try:
        x = tmp[::-1]
        insert(root, x)
      except:
        nfg = 0

print "trie constructed"

find_morphenes(root, "",10)
find_words(root , "")


# for small files
pickle.dump( morphenes, open( "all_prefixmorphenes.p", "wb" ) )     # suffix and its set



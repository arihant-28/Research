from gensim.models import Word2Vec,word2vec
from  sys import stdin
import cPickle as pickle
import os
import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

class MySentences(object):
  def __init__(self, dirname):
    self.dirname = dirname

  def __iter__(self):
    for fname in os.listdir(self.dirname):
      for line in open(os.path.join(self.dirname, fname)):
        yield line.split()

sentences = MySentences('directory_path/')

model = Word2Vec(sentences, size=300, window =5 ,  min_count=5, workers= 500 , sg = 1)

model.save("w2v.txt")


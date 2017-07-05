Before executing each python file, kindly open the file 
and mention the file path explicity in each input space - each input space is verbosed with what kind of input it expects.


In TRAIN/

python trainSG.py

(specify directory path in the code: line 17)
-----------------------

In freq/

python freq.py < corpus_path

(pickles frequency dict)
------------------------

In TRIE/

all_trie.py < corpus_path
all_prefixtrie.py < corpus_path

When these two are completed

python generate_transitions.py
python prefixgenerate_transitions.py

-------------------------

In morph_set/

python make_sets.py

--------------------------

In exp/

python language.py < corpus_path > target_path

---------------------------

In TEST/

python test_all.py

---------------------------

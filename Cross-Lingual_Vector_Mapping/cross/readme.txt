Before executing each python file, kindly open the file
and mention the file path explicity in each input space - each input space is verbosed with what kind of input it expects.

In TRAIN/

python trainSG.py

(specify directory path in the code: line 17)

--------------------------------

python one2one.py

where
fmodel = target language model
emodel = source language model
ffreq = frequency dict of target model
efreq = frequency dict of source model
f1 = parallel corpus
f2 = fast_align alignments

--------------------------------

In test/

python test_biz.py 

-----------------------------

#!/usr/bin/python

from os import environ, path
from sys import stdout
import sys
import os
from pocketsphinx import *
from sphinxbase import *

path_to_directory = "../td_corpus_digits/SNR35dB"
out_path = "results_td_corpus_digits"
if not os.path.isdir(out_path):
    os.mkdir(out_path)
    print('directory created:',out_path)
types = ['man', 'woman', 'boy', 'girl']
for type in types:
    path = os.path.join(out_path, type)
    if not os.path.isdir(path):
        os.mkdir(path)
seqfiles = ['seq1digit_200_files', 'seq3digits_100_files', 'seq5digits_100_files']
for type in types:
    for seqfile in seqfiles:
        path = os.path.join(out_path, type, seqfile)
        if not os.path.isdir(path):
            os.mkdir(path)
in_paths = []
in_files= list()
ref_files = list()
out_files = list()
dico = dict()
for type in types:
    for seq in seqfiles:
        directory = os.path.join(path_to_directory, type, seq)
        for element in os.listdir(directory):
            if element.endswith('.raw'):
                infile = os.path.join(directory, element)
                in_files.append(infile)
                ref_file = os.path.join(infile[0:-4]+'.ref')
                ref_files.append(ref_file)
                out_file = os.path.join('./'+out_path, type, seq, element[0:-4]+'results.txt')
                out_files.append(out_file)
                dico[element[0:-4]] = (infile, ref_file, out_file)

# print(in_files)
# print(ref_files)
# print(dico)
# sys.exit()

# sys.exit()

# Create a decoder with certain model
config = Decoder.default_config()
config.set_string('-hmm',  '../ps_data/model/en-us')
config.set_string('-lm',   '../ps_data/lm/turtle.lm.bin')
config.set_string('-dict', '../ps_data/lex/turtle.dic')
decoder = Decoder(config)

# Decode with lm
# decoder.start_utt()
# for infile, ref_file, out_file in dico:
#     stream = open(infile, 'rb')
#     while True:
#         buf = stream.read(1024)
#         if buf:
#              decoder.process_raw(buf, False, False)
#         else:
#              break
#     decoder.end_utt()
# print ('Decoding with "turtle" language:', decoder.hyp().hypstr)
#
# print ('')
# print ('--------------')
# print ('')

# Switch to JSGF grammar
# jsgf = Jsgf('ps_data/jsgf/threedigits.gram')
# rule = jsgf.get_rule('numbers.sequence1')
# rule2 = jsgf.get_rule('numbers.sequence3')
# rule3 =jsgf.get_rule('numbers.sequence5')
# fsg = jsgf.build_fsg(rule, decoder.get_logmath(), 7.5)
# fsg.writefile('3numbers.fsg')
#
# decoder.set_fsg("3numbers", fsg)
# decoder.set_search("3numbers")
#
# decoder.start_utt()
for k, v in dico.items():
    if str(k)[-10] == '1':
        num = 1
        print(num, k)
        # break
    if str(k)[-11] == '5':
        num = 5
        print(num, k)
    if str(k)[-11] == '3':
        num = 3
        print(num, k)
    infile = v[0]
    ref_file = v[1]
    out_file = v[2]
    jsgf = Jsgf('../ps_data/jsgf/threedigits.gram')
    rule = jsgf.get_rule('numbers.sequence%s' % num)
    fsg = jsgf.build_fsg(rule, decoder.get_logmath(), 7.5)
    fsg.writefile('3numbers.fsg')

    decoder.set_fsg("3numbers", fsg)
    decoder.set_search("3numbers")

    decoder.start_utt()
    stream = open(infile, 'rb')
    while True:
        buf = stream.read(1024)
        if buf:
             decoder.process_raw(buf, False, False)
        else:
             break

    with open(out_file, 'w') as f:
        with open(ref_file, 'r') as f2:
            ref = f2.read()
        if decoder.hyp():
            decoder.hyp().hypstr
            f.write(str(decoder.hyp().hypstr))
            f.write('\n')
            f.write(ref)
    print ('Decoding with "numbers" grammar:', decoder.hyp().hypstr)
    decoder.end_utt()

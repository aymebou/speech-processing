#!/usr/bin/python

from os import environ, path
from sys import stdout

from pocketsphinx import *
from sphinxbase import *

# Create a decoder with certain model
config = Decoder.default_config()
config.set_string('-hmm',  'ps_data/model/en-us')
jsgf = Jsgf('ps_data/jsgf/numbers.gram')

def decoder_config_jsgf():
    config.set_string('-lm',   'ps_data/lm/turtle.lm.bin')
    config.set_string('-dict', 'ps_data/lex/turtle.dic')
    return Decoder(config)


def decoder_config_ngram():
    config.set_string('-lm',   'ps_data/lm/en-us.lm.bin')
    config.set_string('-dict', 'ps_data/lex/cmudict-en-us.dict')
    return Decoder(config)


def create_file_list(
        types = ['man', 'woman', 'boy', 'girl'],
        digits = [1, 3, 5],
        noise_levels = [ 'low' ]
        ):
    path_to_directory = "td_corpus_digits/"
    noise_level_folder_name = { "low": "SNR35dB", "medium": "SNR25dB", "high": "SNR15dB", "huge": "SNR05dB", }
    noise_levels_folders = [ noise_level_folder_name[i] for i in noise_levels ]
    digit_folder_names = {1: 'seq1digit_200_files', 3: 'seq3digits_100_files', 5: 'seq5digits_100_files'}
    digit_folders = [ digit_folder_names[i] for i in digits ]
    sample_paths = []
    for noise in noise_levels_folders:
        for seq in digit_folders:
            for type in types:
                directory = os.path.join(path_to_directory, noise, type, seq)
                for element in os.listdir(directory):
                    if element.endswith('.raw'):
                        sample_paths.append(os.path.join(directory, element))
    return sample_paths


def decode_sample(sample_path, is_jsgf=True, rule=jsgf.get_rule('numbers.sequence_135')):
    if is_jsgf:
        fsg = jsgf.build_fsg(rule, decoder.get_logmath(), 7.5)
        fsg.writefile('goforward.fsg')
        decoder.set_fsg("goforward", fsg)
        decoder.set_search("goforward")

    decoder.start_utt()
    stream = open(sample_path, 'rb')
    while True:
        buf = stream.read(1024)
        if buf:
             decoder.process_raw(buf, False, False)
        else:
             break
    decoder.end_utt()
    if not decoder.hyp():
        return ''
    return decoder.hyp().hypstr


def compute_error_rate_from_model(types, number_lengths, noise_levels, jsgf=True, rule=jsgf.get_rule('numbers.sequence_135')):
    errror_count = 0
    sample_paths = create_file_list(types, number_lengths, noise_levels)
    for sample in sample_paths:
        hyp = decode_sample(sample, jsgf, rule)
        if not hyp == ref(sample):
            errror_count+=1
    return errror_count/len(sample_paths)


def compute_error_rate_from_response_dict(response_dict, types, number_lengths, noise_levels, jsgf=True, rule=jsgf.get_rule('numbers.sequence_135')):
    errror_count = 0
    sample_paths = create_file_list(types, number_lengths, noise_levels)
    for sample in sample_paths:
        hyp = decode_sample(sample, jsgf, rule)
        if not hyp == ref(sample):
            errror_count+=1
    return errror_count/len(sample_paths)


def make_response_dict():
    sample_paths = create_file_list()
    response_dict = {}
    for s in sample_paths:
        hyp = decode_sample(s)
        response_dict[s] = hyp
    return response_dict


def ref(sample):
    return open(sample[:-3] + 'ref', 'r').read().strip()

## wers
wer = {}

#model

decoder = decoder_config_ngram()
wer['ngram'] = compute_error_rate_from_model(['man'], [1, 3, 5], ['low', 'medium', 'high', 'huge'], False)

decoder = decoder_config_jsgf()
wer['jsgf_seq_135'] = compute_error_rate_from_model(['man'], [1, 3, 5], ['low', 'medium', 'high', 'huge'])

rule = jsgf.get_rule('numbers.sequence_unknown')
wer['jsgf_seq_unknown'] = compute_error_rate_from_model(['man'], [1, 3, 5], ['low', 'medium', 'high', 'huge'], True, rule)

#speaker group -- in function of sample's amount of number
response_dict = make_response_dict()

wer['girl'] = compute_error_rate_from_response_dict(response_dict, ['girl'], [1, 3, 5], ['low'])
wer['man'] = compute_error_rate_from_response_dict(response_dict, ['man'], [1, 3, 5], ['low'])
wer['woman'] = compute_error_rate_from_response_dict(response_dict, ['woman'], [1, 3, 5], ['low'])
wer['boy'] = compute_error_rate_from_response_dict(response_dict, ['boy'], [1, 3, 5], ['low'])

#length

wer['one_digit'] = compute_error_rate_from_response_dict(response_dict, ['man'], [1], ['low'])
wer['three_digit'] = compute_error_rate_from_response_dict(response_dict, ['man'], [3], ['low'])
wer['five_digit'] = compute_error_rate_from_response_dict(response_dict, ['man'], [5], ['low'])

#noise

wer['man_high_q'] = compute_error_rate_from_response_dict(response_dict, ['man'], [1, 3, 5], ['low'])
wer['man_standard_q'] = compute_error_rate_from_response_dict(response_dict, ['man'], [1, 3, 5], ['medium'])
wer['man_low_q'] = compute_error_rate_from_response_dict(response_dict, ['man'], [1, 3, 5], ['high'])
wer['man_very_low_q'] = compute_error_rate_from_response_dict(response_dict, ['man'], [1, 3, 5], ['huge'])

f = open('Word-Error-Rates.txt', 'w')

f.write('--- MODEL COMPARAISON (all samples) ---\n')
f.write('ngram : ' + str(wer['ngram']) + '\n')
f.write('jsgf_seq_135 : ' + str(wer['jsgf_seq_135']) + '\n')
f.write('jsgf_seq_unknown : ' + str(wer['jsgf_seq_unknown']) + '\n\n\n' )

f.write('--- SPEAKER GROUP COMPARAISON (all very low noise with all digits sequence) ---\n')
f.write('girl : ' + str(wer['girl']) + '\n')
f.write('man : ' + str(wer['man']) + '\n')
f.write('woman : ' + str(wer['woman']) + '\n' )
f.write('boy : ' + str(wer['boy']) + '\n\n\n' )

f.write('---  LENGTH COMPARAISON (all very low noise only for man) ---\n')
f.write('one_digit : ' + str(wer['one_digit']) + '\n')
f.write('three_digit : ' + str(wer['three_digit']) + '\n')
f.write('five_digit : ' + str(wer['five_digit']) + '\n\n\n' )

f.write('--- NOISE COMPARAISON (only man speakers) ---\n')
f.write('man_high_q : ' + str(wer['man_high_q']) + '\n')
f.write('man_standard_q : ' + str(wer['man_standard_q']) + '\n')
f.write('man_low_q : ' + str(wer['man_low_q']) + '\n' )
f.write('man_very_low_q : ' + str(wer['man_very_low_q']) + '\n\n\n' )


f.close()

from jiwer import wer:

reslts_path = "results_td_corpus_digits"




            man_results.append(wer)

            woman_results.append(wer)

            boy_results.append(wer)

            girl_results.append(wer)

    averagemen = sum(man_results)/len(man_results)
    averagewom = sum(woman_results)/len(woman_results)
    averagegir = sum(girl_results)/len(girl_results)
    averageboy = sum(boy_results)/len(boy_results)
with open('results.txt', 'w') as f:

    f.write('average results man '+str(averagemen))
    f.write('\n')
    f.write('average results woman: '+str(averagewom))
    f.write('\n')
    f.write('average results boy: '+str(averageboy))
    f.write('\n')
    f.write('average results girl: '+str(averagegirl))

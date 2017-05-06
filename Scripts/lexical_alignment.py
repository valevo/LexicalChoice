import refexps
from os import listdir, path, mkdir, stat
from itertools import combinations
from collections import defaultdict
import numpy as np
import nltk
from scipy import stats
from random import shuffle
import compound_splitter
import pickle


def compute_values_move(refexps_dir, output_file, compound = True, random = False):
    '''
    compute lexical alignment for a set of task-oriented dialogues and write it to an output file
    :param refexps_dir: directory with referring expressions 
    :param output_file: output file for results
  
    '''    
    splits = compound_splitter.load_dict('de_lower.dict')
    move_alignment = defaultdict(list)
    random_alignment = defaultdict(list)
    for dialogue in listdir(refexps_dir):
        #extract dialogue type
        if dialogue.startswith('FTT'):
            language = 'german'
        else:
            language = 'english'
        dialogue = path.join(refexps_dir, dialogue)
        #load referring expressions data
        dialogue = refexps.load_data(dialogue)
        #move level
        if random == False:
            dialogue_move = refexps.move_level(dialogue)
        else:
            dialogue_move = dialogue
        #iterate over moves
        for move in dialogue_move:
            refs = move[1]
            move_id = move[0]
            #iterate over objects
            for obj in refs:
                #iterate over objects
                refobj = refs[obj]
                #SIMILARITY OF LEXICAL CONTENT INTO
                total_words = 0
                total_words_speaker = defaultdict(int)
                sameword_n = 0
                sameword_n_speaker = defaultdict(int)
                speakers = set()
                prev_words = set()
                for ref in refobj:
                    speaker = ref[1]
                    words = refexps.lex_material(ref, language, splits, compound)
                    if prev_words != set():
                        for w in words:
                            if w in prev_words:
                                sameword_n += 1
                                sameword_n_speaker[speaker] += 1
                    else:
                        starter = speaker
                        first_words = len(words)
                    speakers.add(speaker)
                    total_words_speaker[speaker] += len(words)
                    total_words += len(words)
                    for w in words:
                        prev_words.add(w)
                if (total_words - first_words) != 0:
                    alignment = float(sameword_n)/float(total_words - first_words)
                    move_alignment['Alignment'].append(alignment)
                for s in speakers:
                        if starter == s:
                            if (total_words_speaker[s] - first_words) != 0:
                                alignment = float(sameword_n_speaker[s])/float(total_words_speaker[s] - first_words)
                                move_alignment['Alignment '+s].append(alignment)
                        else:
                            if(total_words_speaker[s]) != 0:
                                alignment = float(sameword_n_speaker[s])/float(total_words_speaker[s])
                                move_alignment['Alignment '+s].append(alignment)
    for value in move_alignment:
        dataset = move_alignment[value]
        output_file.write( '\n'+value + ': ')
        output_file.write('\nMean: '+ str(np.mean(dataset)) +'\tStandard deviation: '+ str(np.std(dataset)))
        output_file.write('\nMax value: ' + str(max(dataset)) + '\tMin value: '+ str(min(dataset)))
    return move_alignment

if __name__== "__main__":
	de_dataset_dir = 'En_De_Dataset/De/RefExp'
	en_dataset_dir = 'En_De_Dataset/En/RefExp'
	all_dataset_dir = 'En_De_Dataset/All/RefExp'
	output_file = open('Results/LexAlignment_analysis.txt', 'w')
	output_file.write('\n\n---German---\n\n')
	results_de = compute_values_move(de_dataset_dir, output_file)
	output_file.write('\n\n---English---\n\n')
	results_en = compute_values_move(en_dataset_dir, output_file)
	output_file.write('\n\n---English and German---\n\n')
	results_all = compute_values_move(all_dataset_dir, output_file)
	output_file.write('\n\n\n\n---Random---\n\n\n\n')
	random_all_dir = 'En_De_Dataset/All/Random_RefExp'
	results_random_all = compute_values_move(random_all_dir, output_file, random = True)
	output_file.write('\n\nSignificant differences with random:\n')
	for var in results_all:
	    mannwhitneyu =  stats.mannwhitneyu(results_all[var],results_random_all[var], alternative='two-sided')
	    if mannwhitneyu[1] < 0.05:
		output_file.write(var + '\n')
		output_file.write( str(mannwhitneyu) + '\n')
		output_file.write('All: ' + str(np.mean(results_all[var])) + '\tRandom: ' + str(np.mean(results_random_all[var]))+'\n')
	output_file.write('\n\n\n\n---German without compound splitter---\n\n\n\n')
	results_de_nocs = compute_values_move(de_dataset_dir,  output_file, compound = False)
	output_file.write('\n\n')
	output_file.write('\n\nSignificant differences with and without compound splitter:\n')
	for var in results_de:
	    mannwhitneyu =  stats.mannwhitneyu(results_de[var],results_de_nocs[var], alternative='two-sided')
	    if mannwhitneyu[1] < 0.05:
		output_file.write(var+ '\n')
		output_file.write( str(mannwhitneyu)+ '\n')
		output_file.write('With compound splitter: ' + str(np.mean(results_de[var])) + '\Without: ' + str(np.mean(results_de_nocs[var]))+'\n')
	output_file.write('\n\nSignificant differences between languages:\n')
	for var in results_all:
	    mannwhitneyu =  stats.mannwhitneyu(results_de[var],results_en[var], alternative='two-sided')
	    if mannwhitneyu[1] < 0.05:
		output_file.write(var+ '\n')
		output_file.write( str(mannwhitneyu)+ '\n')
		output_file.write('German: ' + str(np.mean(results_de[var])) + '\English: ' + str(np.mean(results_en[var]))+'\n')

	output_file.write('\n\nSignificant differences between players:\n')
	mannwhitneyu =  stats.mannwhitneyu(results_de['Alignment e-utts'],results_de['Alignment p-utts'], alternative='two-sided')
	if mannwhitneyu[1] < 0.05:
	    output_file.write('Alignment de\n')
	    output_file.write(str(mannwhitneyu)+ '\n')
	    output_file.write('p: ' + str(np.mean(results_de['Alignment p-utts'])) + '\e: ' + str(np.mean(results_de['Alignment e-utts']))+'\n')

	mannwhitneyu =  stats.mannwhitneyu(results_en['Alignment e-utts'],results_en['Alignment p-utts'], alternative='two-sided')
	if mannwhitneyu[1] < 0.05:
	    output_file.write('Alignment en\n')
	    output_file.write(str(mannwhitneyu)+'\n')
	    output_file.write('p: ' + str(np.mean(results_en['Alignment p-utts'])) + '\e: ' + str(np.mean(results_en['Alignment e-utts']))+'\n')
		                                                                
	mannwhitneyu =  stats.mannwhitneyu(results_all['Alignment e-utts'],results_all['Alignment p-utts'], alternative='two-sided')
	if mannwhitneyu[1] < 0.05:
	    output_file.write('Alignment all\n')
	    output_file.write(str(mannwhitneyu)+'\n')
	    output_file.write('p: ' + str(np.mean(results_all['Alignment p-utts'])) + '\e: ' + str(np.mean(results_all['Alignment e-utts']))+'\n')
	output_file.close()

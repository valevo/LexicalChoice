from refexps import load_data, move_level, gamerun_level, get_previous #, lex_sim
from os import listdir, path
from itertools import combinations
from collections import defaultdict
import numpy as np
from scipy import stats
import compound_splitter
from scipy import stats
from nltk import word_tokenize
from string import punctuation
punct = list(punctuation)

def exp_len(exp, language, splits, compound):
    '''
    Tokenization and compound splitting
    :param exp: referring expression tuple
    :return: set of tokens of the phrase
    '''
    exp = exp[2]
    words = word_tokenize(exp, language)
    if compound == True:
        if language == 'german':
            words_nocomp = []
            for w in words:
                word = compound_splitter.split_word(w, splits)
                words_nocomp = words_nocomp + (word.split(' '))	
                words = words_nocomp
    return len(words)

def len_div(exp1, previous, language, splits, compound):
    '''
    compute length decrease of a referring expression with respect to the previous ones
    :param exp1: referring expression tuple 1
    :param exp2: previous referring expressions
    :return: length decrease
    '''        
    len_exp = exp_len(exp1, language, splits, compound)    
    previous_len = np.mean(previous)
    metric = float(previous_len - len_exp)/float(previous_len + len_exp)
    return metric if not np.isnan(metric) and metric > -1  and metric < 1 else 'undefined'

def compute_values_move(refexps_dir, output_file, compound = True, random = False):
    '''
    compute length decrease values for a set of task-oriented dialogues and write it to an output file
    :param refexps_dir: directory with referring expressions 
    :param output_file: output file for results
  
    '''    
    splits = compound_splitter.load_dict('de_lower.dict')
    move_alignment = defaultdict(list)

    for dialogue in listdir(refexps_dir):
        if dialogue.startswith('FTT'):
            language = 'german'
        else:
            language = 'english'
        dialogue = path.join(refexps_dir, dialogue)
        #load referring expressions data
        dialogue = load_data(dialogue)
        #move level
        if random == False:
            dialogue_move = move_level(dialogue)
        else:
            dialogue_move = dialogue
        for move in dialogue_move:
            refs = move[1]
            #iterate over objects
            for obj in refs:
                #iterate over objects
                refobj = refs[obj]
                #SIMILARITY OF LEXICAL CONTENT INTO
                prev_length = []
                speakers = set()
                divs = []
                divs_speakers = defaultdict(list)
                for ref in refobj:
                    speaker = ref[1]
                    speakers.add(speaker)
                    if prev_length != []:
                        div = len_div(ref, prev_length, language, splits, compound)
                        if div != 'undefined':
                            divs.append(div)
                            divs_speakers[speaker].append(div)
                    len_exp = exp_len(ref, language, splits, compound) 
                    prev_length.append(len_exp)
                if divs != []:
                    alignment = np.mean(divs)
                    move_alignment['Alignment'].append(alignment)
                for s in speakers:
                    if divs_speakers[speaker] != []:
                        alignment = np.mean(divs_speakers[speaker])
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
	output_file = open('Results/LenDecrease_analysis.txt', 'w')
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
	

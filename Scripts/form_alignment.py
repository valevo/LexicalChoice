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
    compute syntactic alignment for a set of task-oriented dialogues and write it to an output file
    :param refexps_dir: directory with referring expressions 
    :param output_file: output file for results
  
    '''    
    move_alignment = defaultdict(list)
    for dialogue in listdir(refexps_dir):
        dialogue = path.join(refexps_dir, dialogue)
        dialogue = refexps.load_data(dialogue)
        #move level
        if random == False:
            dialogue_move = refexps.move_level(dialogue)
        else:
            dialogue_move = dialogue
        speakers = set()
        for move in dialogue_move:
            refs = move[1]
            for obj in refs:
                refobj = refs[obj]
                align_speaker = {}
                total_n = len(refs[obj])
                sameform_n = 0
                sameform_n_speaker = defaultdict(int)
                total_n_speaker = defaultdict(int)
                prev_forms = set()
                for ref in refs[obj]:
                    form = ref[3]
                    speaker = ref[1]
                    if prev_forms != set():
                        if form in prev_forms:
                            sameform_n += 1
                            sameform_n_speaker[speaker] += 1
                    else:
                        starter = speaker
                    speakers.add(speaker)
                    total_n_speaker[speaker] += 1
                    prev_forms.add(form)
                if (total_n - 1) != 0:
                    alignment = float(sameform_n)/float(total_n - 1)
                    move_alignment['Alignment'].append(alignment)
                for s in speakers:
                        if starter == s:
                            if (total_n_speaker[s] - 1) != 0:
                                alignment = float(sameform_n_speaker[s])/float(total_n_speaker[s] - 1)
                                move_alignment['Alignment '+s].append(alignment)
                        else:
                            if(total_n_speaker[s]) != 0:
                                alignment = float(sameform_n_speaker[s])/float(total_n_speaker[s])
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
	output_file = open('Results/FormAlignment_analysis.txt', 'w')
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

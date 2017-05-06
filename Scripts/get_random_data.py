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

def get_random_data(refexps_dir):
    random_dir = path.join(refexps_dir.replace('RefExp', ''), 'Random_RefExp')
    try:
        stat(random_dir)
    except:
        mkdir(random_dir)
    for dialogue in listdir(refexps_dir):
        dialogue_id = dialogue
        dialogue = path.join(refexps_dir, dialogue)
        dialogue = refexps.load_data(dialogue)
        dialogue_move = refexps.move_level(dialogue)
        ref_move_objects = defaultdict(dict)
        all_ref_objects = defaultdict(list)
        for move in dialogue_move:
            refs = move[1]
            move_id = move[0]
            for obj in refs:
                ref_move_objects[move_id][obj] = len(refs[obj])
                for ref in refs[obj]:
                    all_ref_objects[obj].append(ref)
        random_ref_objects = {}
        for obj in all_ref_objects:
            shuffle(all_ref_objects[obj])
        random_move = []
        for move in dialogue_move:
            move_id, refs = move
            objects_move = refs.keys()
            new_refs = defaultdict(list)
            for o in objects_move:
                obj_toadd = ref_move_objects[move_id][o]
                for i in xrange(obj_toadd):
                    ref = all_ref_objects[o][0]
                    new_refs[o].append(all_ref_objects[o][0])
                    all_ref_objects[o].remove(ref)
            random_move.append((move_id, new_refs))
        pickle.dump(random_move, open(path.join(random_dir, dialogue_id)+ '.p', 'w'))
 
if __name__ == '__main__':       
	get_random_data('En_De_Dataset/All/RefExp')

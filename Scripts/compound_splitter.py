#!/usr/bin/python

import sys
import fileinput
import argparse

def load_dict(file):
    splits = {}
    with open(file) as f:
        for line in f:
            es = line.decode('utf8').rstrip('\n').split(" ")
            w = es[0]
            indices = map(lambda i: i.split(','), es[1:])

            splits[w] = []
            for from_, to, fug in indices:
                s, e = int(from_), int(to)
                # Don't use single character splits - just add to prev split
                if e - s == 1:
                    splits[w][-1][1] += 1
                else:
                    splits[w].append([s, e, fug])
    return splits

def split_word(w, splits):
	if w in splits:
		w_split = []
	    	for from_, to, fug in splits[w]:
	   		wordpart = w[from_:to-len(fug)]
	    		wordpart = wordpart.lower()
			w_split.append(wordpart)

	    	return u" ".join(w_split)
	else:
	    return w



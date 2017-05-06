from refexps import extract_info
import xml.etree.ElementTree as ET
from collections import defaultdict
from os import path, listdir, makedirs, stat
import re
import pickle


if __name__ == '__main__':
	data_folder = 'PentoCorpora'
	games = listdir(data_folder)
	print games
	for g in games:
	    folder = path.join(data_folder, g)
	    basedata = path.join(folder, 'Basedata')
	    markables = path.join(folder,'Markables')
	    dialogues = []
	    output_folder = g.replace('/', '.')
	    output_folder = path.join('Dataset', output_folder)
	    for doc in listdir(basedata):
		if doc.endswith('_words.xml'):
		    dialogue = doc.replace('_words.xml', '')
		    dialogues.append(dialogue)
	    try:
		stat(output_folder)
	    except:
		makedirs(output_folder)
	    try:
		stat(output_folder+ '/RefExp')
	    except:
		makedirs(output_folder+ '/RefExp')
	    try:
		stat(output_folder+ '/Success')
	    except:
		makedirs(output_folder+ '/Success')
	    for d in dialogues:
		try: 
		    r, s = extract_info(d)
		    pickle.dump(r, open( path.join(output_folder + '/RefExp', d + "_refexps.p"), "wb" ) )
		    pickle.dump(s, open( path.join(output_folder + '/Success', d + "_movesuccess.p"), "wb" ) )
		    print d
		except:
		    pass

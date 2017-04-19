import xml.etree.ElementTree as ET
from collections import defaultdict
from os import path, listdir, makedirs, stat
import re
import compound_splitter
import pickle

def extract_info(dialogue):
    '''
    :param dialogue: dialogue name
    :return: list with referring expressions per move, per speaker, per object, per reference type (ordered)
    '''
    words_tree = ET.parse(path.join(basedata, dialogue + '_words.xml'))
    words_root = words_tree.getroot()
    words = {}
    for word in words_root:
        words[int(word.attrib['id'].strip('word_'))] = word.text
    #moves
    moves_tree = ET.parse(path.join(markables, dialogue + '_move_markables.xml'))
    moves_root = moves_tree.getroot()
    moves_spans = defaultdict(list)
    success_move = {}
    i = 0
    for move in moves_root:
        id_move = move.attrib['span'].replace('word_', '').split('..')
        try:
            success = move.attrib['move_world']
        except:
            success = move.attrib['world']
        if len(id_move) == 2:
            id_move = (int(id_move[0]), int(id_move[1]))
        else:
            id_move = (int(id_move[0]), int(id_move[0]))
        moves_spans[i] = id_move
        success_move[id_move] = success
        i += 1
    utt_tree = ET.parse(path.join(markables, dialogue + '_utterance_markables.xml'))
    utts_root = utt_tree.getroot()
    utts_speaker = defaultdict(list)
    for utt in utts_root:
        span =  utt.attrib['span'].replace('word_', '').split('..')
        if len(span) == 2:
            span = (int(span[0]), int(span[1]))
        else:
            span = (int(span[0]), int(span[0]))
        speaker =  utt.attrib['speaker']
        utts_speaker[speaker].append(span)
    #associate referring expressions to objects
    ref_tree = ET.parse(path.join(markables, dialogue + '_ref_markables.xml'))
    refs_root = ref_tree.getroot()
    refs_objects = defaultdict(list)
    for ref in refs_root:
        ref_type = ref.attrib['referent_type']
        form =  ref.attrib['form']
        span =  ref.attrib['span'].replace('word_', '').split('..')
        if len(span) == 2:
            span = (int(span[0]), int(span[1]))
        else:
            span = (int(span[0]), int(span[0]))
        try:
            item =  ref.attrib['item_id']
            refs_objects[item].append((span, form, ref_type))
        except:
            pass
    moves_utt = defaultdict(dict)
    for s in utts_speaker:
        for utt in utts_speaker[s]:
            for m in moves_spans:
                if utt[0] >= moves_spans[m][0] and utt[0] <= moves_spans[m][1]:
                    if not moves_utt[moves_spans[m]].has_key(s):
                        moves_utt[moves_spans[m]][s] = []
                    moves_utt[moves_spans[m]][s].append(utt)
    moves_ref = defaultdict(dict)
    for obj in refs_objects:
        speaker = ''
        move = ''
        for ref in refs_objects[obj]:
            word_span = ref[0]
            for m in moves_utt:
                for s in moves_utt[m]:
                    for utt in moves_utt[m][s]:
                        if word_span[0] >= utt[0] and word_span[0] <= utt[1]:
                            speaker = s
                            move = m
                            if not moves_ref[move].has_key(speaker):
                                moves_ref[move][speaker] = {}
                            if not moves_ref[move][speaker].has_key(obj):
                                moves_ref[move][speaker][obj] = []
                            moves_ref[move][speaker][obj].append(ref)
                            break
    moves_ref_words = defaultdict(dict)
    for m in moves_ref:
        for s in moves_ref[m]:
            for o in moves_ref[m][s]:
                for ref in moves_ref[m][s][o]:
                    span = ref[0]
                    form = ref[1]
                    ref_type = ref[2]
                    if len(span) == 1:
                        exp = words[span[0]]
                    else:
                        exp = ''
                        i = span[0]
                        while i <= span[1]:
                            if i != span[1]:
                                exp += words[i] + ' '
                            else:
                                exp += words[i]
                            i += 1
                    if not moves_ref_words[m].has_key(s):
                        moves_ref_words[m][s] = {}
                    if not moves_ref_words[m][s].has_key(o):
                        moves_ref_words[m][s][o] = {}
                    if not moves_ref_words[m][s][o].has_key(ref_type):
                        moves_ref_words[m][s][o][ref_type] = []
                    #remove hesitations, and internal tags
                    exp = re.sub(r'<.*>', '', exp)
                    exp = re.sub(r'</.*>', '', exp)
                    exp = re.sub(r'\(.*\)', '', exp)
                    exp = re.sub(r'[\(\)\[\]\.]','', exp)
                    exp = exp.lower()
                    exp_sp = exp.split(' ')
                    if len(exp_sp) == 1 and exp.endswith("'s"):
                        exp = exp.replace("'s", '')
                    moves_ref_words[m][s][o][ref_type].append((exp, span, form))
            for t in moves_ref_words[m][s][o]:
                moves_ref_words[m][s][o][t] = sorted(moves_ref_words[m][s][o][ref_type], key=lambda tup: tup[1][0])
    moves_ref_words = sorted(moves_ref_words.items())
    return moves_ref_words, success_move

def load_data(dialogue_path):
    '''
    Load pickle file of the dialogue
    :param dialogue_path: dialogue refexps filepath
    :return: list with referring expressions
    '''
    with open(dialogue_path) as handle:
        d = pickle.load(handle)
    return d

def move_level(d_refexps):
    '''
    Restructure data in order to get info about refexps usage at the move level
    :param d_refexps: list with reffering expressions as output in extract_info
    :return: list with referring expressions per move, per object (object + reference type) [speaker is given in the tuple]
    '''
    new = {}
    for m in d_refexps:
        move, d = m
        for s in d:
            for o in d[s]:
                for r in d[s][o]:
                    for exp in d[s][o][r]:
                        if not new.has_key(move):
                            new[move] = {}
                        if not new[move].has_key((o,r)):
                            new[move][(o,r)] = []
                        text, span, form = exp
                        exp = (span, s, text, form)
                        new[move][(o,r)].append(exp)
        for t in new[move]:
            new[move][t] = sorted(new[move][t], key=lambda tup: tup[0][0])
    new = sorted(new.items())
    return new

def get_previous(refexp, obj_refexps):
    '''
    Outputs the last referring expression used for that object by the other speaker
    :param refexp: referring expression tuple
    :param obj_refexps: list of referring expressions for that object
    :return:
    '''
    i = obj_refexps.index(refexp) - 1
    speaker = refexp[1]
    previous = 'no_previous'
    while i >= 0:
        if obj_refexps[i][1] != speaker:
            previous = obj_refexps[i]
            break
        i =- 1
    return previous

from nltk.corpus import stopwords
from nltk import word_tokenize
from nltk.stem.snowball import SnowballStemmer

from string import punctuation
punct = list(punctuation)

def lex_material(exp, language, splits, compound):
    '''
    Extract content words by the phrase
    :param exp: referring expression tuple
    :return: set of content words of the phrase
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
    content_words = set()
    stemmer = SnowballStemmer(language)
    ignore_words = stopwords.words(language)
    ignore_words.append('dis')
    for w in words:
        w = stemmer.stem(w)
        if not w in punct:
            stopword = False
            for sw in ignore_words:
                if sw == w:
                    stopword = True
            if stopword == False:
                content_words.add(w)
    return content_words

def init_compounds(de_dict):
    splits = compound_splitter.load_dict(de_dict)
    return splits

def lex_sim(exp1, exp2, language, splits, compound = True):
    '''
    compute dice similarity between the content words in two referring expression
    :param exp1: referring expression tuple 1
    :param exp2: referring expression tuple 2
    :return: dice similarity between the content words in the expressions; undefined if they have none
    '''
    words1 = lex_material(exp1, language, splits, compound)
    words2 = lex_material(exp2, language, splits, compound)
    try:
        dice_sim = float(2*len(words1.intersection(words2)))/float(len(words1)+ len(words2))
    except:
        dice_sim = 'undefined'
    return dice_sim

def gamerun_level(d_refexps):
    '''
    Restructure data in order to get info about refexps usage at the gamerun level (ignore info about moves)
    :param d_refexps: list with reffering expressions as output in extract_info
    :return: list with referring expressions er object (object + reference type) [speaker is given in the tuple]
    '''
    new = {}
    for m in d_refexps:
        move, d = m
        for s in d:
            for o in d[s]:
                for r in d[s][o]:
                    for exp in d[s][o][r]:
                        if not new.has_key((o,r)):
                            new[(o,r)] = []
                        text, span, form = exp
                        exp = (span, s, text, form)
                        new[(o,r)].append(exp)
    for t in new:
        new[t] = sorted(new[t], key=lambda tup: tup[0][0])
    return new


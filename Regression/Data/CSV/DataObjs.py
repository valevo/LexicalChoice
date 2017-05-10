import pickle
import matplotlib.pyplot as plt

class Move:
    def __init__(self, move_struct, move_id=None, succs_map=None, conf_map=None):
        self.succs_lvl = succs_map(move_struct[0]) if succs_map else move_struct[0]
        self.conf_lvl = conf_map(move_struct[1]) if conf_map else move_struct[1]
        self.length = move_struct[2]
        self.len_all = move_struct[3][0]
        self.len_p = move_struct[3][1]
        self.len_e = move_struct[3][2]

        self.lex_all = move_struct[4][0]
        self.lex_p = move_struct[4][1]
        self.lex_e = move_struct[4][2]

        self.form_all = move_struct[5][0]
        self.form_p = move_struct[5][1]
        self.form_e = move_struct[5][2]

        self.move_id = move_id


class Corpus:
    def __init__(self, move_dict = None, succs_map=None, conf_map = None):
        if move_dict is None:
            self.moves = []
        else:
            self.moves = [Move(mv_struct, move_id=mv_id, succs_map=succs_map, conf_map=conf_map)
                         for mv_id, mv_struct in move_dict.iteritems()]

    def merge_with(self, other_corpus):
        self.moves.extend(other_corpus.moves)
        
        
    def set_language(self, lang_str):
        self.lang = lang_str
    
    def attach_lang_info(self):
        for mv in self.moves:
            mv.lang = self.lang
        
    def get_succs(self):
        return [mv.succs_lvl for mv in self.moves]

    def get_confs(self):
        return [mv.conf_lvl for mv in self.moves]
    
    def __len__(self):
        return len(self.moves)

def success_transform(lvl_str):
    if lvl_str == 'correct':
        return 1
    if lvl_str == 'not_moved':
        return 0
    if lvl_str == 'incorrect':
        return -1

    return None

def confidence_transform(lvl_str):
    if lvl_str == 'confident':
        return 4
    if lvl_str == 'reconfirm':
        return 3
    if lvl_str == 'on_hold':
        return 2
    if lvl_str == 'unconfident':
        return 1

    return None

if __name__ == '__main__':
    with open('data_regression.p') as handle:
        all_data = pickle.load(handle)

        de_corp = Corpus(all_data[0], succs_map=None, conf_map=None)
        en_corp = Corpus(all_data[1], succs_map=success_transform, conf_map=None)

        de_len_alls = [mv.len_all for mv in de_corp.moves]
        de_len_ps = [mv.len_p for mv in de_corp.moves]
        de_len_es = [mv.len_e for mv in de_corp.moves]

        print [len(ls) for ls in de_len_alls]
        print [len(ls) for ls in de_len_ps]
        print [len(ls) for ls in de_len_es]

        de_lex_alls = [mv.lex_all for mv in de_corp.moves]
        de_lex_ps = [mv.lex_p for mv in de_corp.moves]
        de_lex_es = [mv.lex_e for mv in de_corp.moves]

        print
        print ([len(ls) for ls in de_lex_alls])
        print ([len(ls) for ls in de_lex_ps])
        print ([len(ls) for ls in de_lex_es])


        plt.hist([len(ls) for ls in de_len_alls], bins=100)
        plt.hist([len(ls) for ls in de_lex_alls], bins=100)

        plt.show()

        plt.hist([len(ls) for ls in de_len_alls], bins=100)
        plt.hist([len(ls) for ls in de_len_es], bins=100)

        plt.show()
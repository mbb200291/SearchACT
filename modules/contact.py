"""
To manage dictionary update operations.

"""
from os import path
import pickle

def save_obj_to_pickle(path, obj): # will end with pickle
    print('# saving file to:', '%s.pickle'%path)
    with open('%s.pickle'%path, 'wb') as f_pkl:
        pickle.dump(obj, f_pkl)

def read_pickle(path_):
    with open(path_, 'rb') as file:
        return pickle.load(file)

class Contact():
    def __init__(self, PATH_DICT_KEY_CONTACT, PATH_DICT_TERM_KEY):
        self.PATH_DICT_KEY_CONTACT = PATH_DICT_KEY_CONTACT
        self.PATH_DICT_TERM_KEY = PATH_DICT_TERM_KEY
        self.DICT_KEY_CONTACT = read_pickle(PATH_DICT_KEY_CONTACT)
        self.DICT_TERM_KEY = read_pickle(PATH_DICT_TERM_KEY)

    def add_searchTerm_to_key(self, str_input_Term, str_input_KEY):
        self.DICT_TERM_KEY.setdefault(str_input_Term, set()).add(str_input_KEY)
        save_obj_to_pickle(path.splitext(self.PATH_DICT_TERM_KEY)[0], self.DICT_TERM_KEY)
        print(f'Successfuly add new search terms. "{str_input_Term}":"{str_input_KEY}"')
        return 0

    def add_contactInfo(self, str_input_KEY, str_add_info):
        self.DICT_KEY_CONTACT[str_input_KEY].append(str_add_info)
        save_obj_to_pickle(path.splitext(self.PATH_DICT_KEY_CONTACT)[0], self.DICT_KEY_CONTACT)
        print(f'Successfuly add new info terms. "{self.DICT_KEY_CONTACT[str_input_KEY]}"')
        return 0
    
    def re_build(self):
        pass
        '''
        import updata_contact
        print('** this operation will wipe out the term created by your own. Sure?')
        str_input = input('\n(Y/N) >>> ').lower()
        if str_input == 'y':
            updata_contact.MakeDict(updata_contact.locate_contact_file())
            DICT_KEY_CONTACT = read_pickle(PATH_DICT_KEY_CONTACT)
            DICT_TERM_KEY = read_pickle(PATH_DICT_TERM_KEY)
        else:
            pass
        '''
    def rm_ifno(self):
        pass
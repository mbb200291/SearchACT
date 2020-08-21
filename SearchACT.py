 #!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Aug  3 23:52:45 2019

@author: linbangqi
@Co-author: somebody
# Version log:
    - 1.0.0
    - 1.1.0:
       - organize by id to value
       - include more keys
    - 1.3.0   
    - 1.3.1
    - 1.4.0: add calculator
    - 1.5.0: Variable name changes; fix width of output table column

# next version
- include removing function

"""

__version__ = '1.5.0'


import pickle
from sys import argv
from os import path

#import sys

def save_obj_to_pickle(path, obj): # will end with pickle
    print('# saving file to:', '%s.pickle'%path)
    with open('%s.pickle'%path, 'wb') as f_pkl:
        pickle.dump(obj, f_pkl)

def read_pickle(path_):
    with open(path_, 'rb') as file:
        return pickle.load(file)


PATH_OF_SCRIPT = path.dirname(argv[0])
PATH_DICT_KEY_CONTACT = path.join(PATH_OF_SCRIPT, r'_DICT_KEY_CONTACTs.pickle')
PATH_DICT_TERM_KEY = path.join(PATH_OF_SCRIPT, '_dict_terms_key.pickle')
DICT_KEY_CONTACT = read_pickle(PATH_DICT_KEY_CONTACT)
DICT_TERM_KEY = read_pickle(PATH_DICT_TERM_KEY)


def add_searchTerm_to_key():
    #from os import path
    #global DICT_KEY_CONTACT
    #global DICT_TERM_KEY
    str_input_KEY = input('Type the E-mail ID (for example, type "benlin" for "benlin@actgenomics.com") or type "exit" to exit.\n>>> ').lower()
    if str_input_KEY in ['EX', 'exit', 'EXIT', 'QUIT']:
        return 0
    elif str_input_KEY not in DICT_KEY_CONTACT.keys():
        print('*** The ID not exist. ***')
        return 0
    str_input_Term = input('Type the new search term or type "exit" to exit.\n>>> ').lower()
    if str_input_Term in ['EX', 'exit', 'EXIT', 'QUIT']:
        return 0
        
    DICT_TERM_KEY.setdefault(str_input_Term.lower(), set()).add(str_input_KEY)
    save_obj_to_pickle(path.splitext(PATH_DICT_TERM_KEY)[0], DICT_TERM_KEY)
    print(f'Successfuly add new search terms. "{str_input_Term}":"{str_input_KEY}"')
    return 0

def add_contactInfo():
    #from os import path
    str_input_KEY = input('Type the E-mail ID (for example, type "benlin" for "benlin@actgenomics.com") or type "exit" to exit.\n>>> ').lower()
    if str_input_KEY in ['EX', 'exit', 'EXIT', 'QUIT']:
        return 0
    elif str_input_KEY not in DICT_KEY_CONTACT.keys():
        print('*** The ID not exist. ***')
        return 0
    
    str_add_info = input('Type the new info of the person or type "exit" to exit.\n>>> ').lower()
    if str_add_info in ['EX', 'exit', 'EXIT', 'QUIT']:
        return 0
    DICT_KEY_CONTACT[str_input_KEY].append(str_add_info)
    save_obj_to_pickle(path.splitext(PATH_DICT_KEY_CONTACT)[0], DICT_KEY_CONTACT)
    print(f'Successfuly add new info terms. "{DICT_KEY_CONTACT[str_input_KEY]}"')
    return 0
def raw_match(str_input, DICT_TERM_KEY, DICT_KEY_CONTACT):
    ## partial matches
    temp_collect = set()
    for i in DICT_TERM_KEY.keys():
        if i.startswith(str_input):
            for k in DICT_TERM_KEY[i]:
                temp_collect.add(k)
    for r in temp_collect:
        print('\n', '>'+'\t'.join(DICT_KEY_CONTACT[r]))
        
    ## within name matches
    print('\n---------------------')
    temp_collect2 = set()
    for i in DICT_TERM_KEY.keys():
        if str_input in i:
            for k in DICT_TERM_KEY[i]:
                temp_collect2.add(k)
    for r in temp_collect2:
        print('\n', '>'+'\t'.join(DICT_KEY_CONTACT[r]))
    if temp_collect==set() and temp_collect2==set():
        print(f'\n "{str_input}" not in list. or type "exit" to exit')
    
# main process
def main():
#    global DICT_KEY_CONTACT, DICT_TERM_KEY,  PATH_DICT_KEY_CONTACT, PATH_DICT_TERM_KEY

    
    while True:
        str_input = input('\n>>> ').lower()
        if str_input in DICT_TERM_KEY:
            ## matched
            for k in DICT_TERM_KEY[str_input]:
                print('\n', '>'+'\t'.join(DICT_KEY_CONTACT[k]))
        
        # add search term function
        elif str_input in ['*addterm', '*add1']:
            print('into adding mode')
            ans = add_searchTerm_to_key()
            if ans == 0:
                pass
            else:
                break

        # add contact info function
        elif str_input in ['*addinfo', '*add2']:
            print('into editing mode')
            ans = add_contactInfo()
            if ans == 0:
                pass
            else:
                break
        # remove contact info function
        elif str_input in ['*rminfo', '*rm2']:
            pass
            """
            print('into editing mode')
            ans = add_contactInfo()
            if ans == 0:
                pass
            else:
                break
            """
        
        elif str_input in ['*rebuild', '*rb']:
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
        elif str_input.startswith('$'):
            print(eval(str_input[1:]))
        elif str_input in ['exit', 'bye', 'ex', 'bye bye', 'quit']:
            break
        elif str_input in ['hi', 'hello']:
            print('HI')
            #break
        # '''
        # elif '+' in str_input:
            str_input = input('\nCalculator >>> ')
            # try:
                # print(eval(str_input))
            # except:
                # print('*** error ***')
        # '''
        elif str_input in ['*help', '*h']:
            print('\n# Type "*addterm", "*add1" to add search term linked to someone. \n# Type "*addinfo" or "*add2" to add additional info to someone. \n# Type "exit", "ex" to leave.')
        else:
            raw_match(str_input, DICT_TERM_KEY, DICT_KEY_CONTACT)


if __name__ == '__main__':
    print('Type part of name to search ACT contact. Type "*help" to get detail instruction. Type "exit" to leave.')
    main()
 #!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Aug  3 23:52:45 2019

@author: linbangqi
@Co-author: bruce

Version log:
- 1.0.0
- 1.1.0:
    - organize by id to value
    - include more keys
- 1.3.0
- 1.3.1
- 1.4.0: add calculator
- 1.5.0: calculator triggering part
- 1.6.0: 
    - caculator loop inside until exit
    - modify a file name for other OS
- 1.7.0:
    - multiple rule syntax
    - calculator re-implement
    - search key by string matching

Next version
- include removing function

"""

__version__ = '1.7.0'


from sys import argv
from os import path
import time
### coustom functions
from modules.tools import save_obj_to_pickle, read_pickle
# caculator
from modules.calculator import cal,parse,handle
###

PATH_OF_SCRIPT = path.dirname(argv[0])
PATH_DICT_KEY_CONTACT = path.join(PATH_OF_SCRIPT, '_dict_key_contacts.pickle')
PATH_DICT_TERM_KEY = path.join(PATH_OF_SCRIPT, '_dict_terms_key.pickle')
DICT_KEY_CONTACT = read_pickle(PATH_DICT_KEY_CONTACT)
DICT_TERM_KEY = read_pickle(PATH_DICT_TERM_KEY)
LI_EXIST_WORDS = ['exit', 'bye', 'ex', 'bye bye', 'quit']

def add_searchTerm_to_key():
    #global DICT_KEY_CONTACT, DICT_TERM_KEY

    str_input_KEY = input('Type the E-mail ID (for example, type "benlin" for "benlin@actgenomics.com") or type "exit" to exit. >>> ').lower()
    if str_input_KEY in LI_EXIST_WORDS:
        return 0
    elif str_input_KEY not in DICT_KEY_CONTACT.keys():
        print('*** The ID not exist. ***')
        return 0
    str_input_Term = input('Type the new search term or type "exit" to exit.\n>>> ').lower()
    if str_input_Term in LI_EXIST_WORDS:
        return 0

    DICT_TERM_KEY.setdefault(str_input_Term.lower(), set()).add(str_input_KEY)
    save_obj_to_pickle(path.splitext(PATH_DICT_TERM_KEY)[0], DICT_TERM_KEY)
    print(f'Successfuly add new search terms. "{str_input_Term}":"{str_input_KEY}"')
    return 0

def add_contactInfo():
    str_input_KEY = input('Type the E-mail ID (for example, type "benlin" for "benlin@actgenomics.com") or type "exit" to exit.\n>>> ').lower()
    if str_input_KEY in LI_EXIST_WORDS:
        return 0
    elif str_input_KEY not in DICT_KEY_CONTACT.keys():
        print('*** The ID not exist. ***')
        return 0

    str_add_info = input('Type the new info of the person or type "exit" to exit.\n>>> ').lower()
    if str_add_info in LI_EXIST_WORDS:
        return 0
    DICT_KEY_CONTACT[str_input_KEY].append(str_add_info)
    save_obj_to_pickle(path.splitext(PATH_DICT_KEY_CONTACT)[0], DICT_KEY_CONTACT)
    print(f'Successfuly add new info terms. "{DICT_KEY_CONTACT[str_input_KEY]}"')
    return 0
    
def search(str_input):
    '''
    Return by the matched keys by str_input.

    '''
    set_match_key = set()
    for term in DICT_TERM_KEY:
        if str_input in term:
            for key in DICT_TERM_KEY[term]:
                set_match_key.add(key)
    return set_match_key

def cal_multi_condi_li(li_ele):
    #print(li_ele)
    li_ele = [x for x in li_ele if x]
    if len(li_ele)==1 and type(li_ele[0])==str:
        return search(li_ele[0])
    elif len(li_ele)==1 and type(li_ele[0])==set:
        return li_ele[0]
    elif len(li_ele)>1 and not [x for x in li_ele if x in ['|', '&']]:
        print('should not exist')
        set_ = set()
        for i in li_ele:
            set_.update(search(i))
        return set_
    else:
        for i in [x for x in li_ele if x in ['|', '&']]:
            offset = li_ele.index(i)
            left, op, right = li_ele[:offset], li_ele[offset:offset+1], li_ele[offset+1:]
            if op == ['&']:
                return cal_multi_condi_li(left) & cal_multi_condi_li(right)
            elif op == ['|']:
                return cal_multi_condi_li(left) | cal_multi_condi_li(right)

def parse_formula(s):
    if s == '':
        return set()
    l = []
    r = []
    s = s.replace(' ','')
    li_element = []
    temp = ''
    for e in s:
        if e == '(':
            li_element.append(temp)
            temp = ''
            l.append(len(li_element))
        elif e == ')':
            li_element.append(temp)
            temp = ''
            r.append(len(li_element))
            li_element[l[-1]:r[-1]+1] = [cal_multi_condi_li(li_element[l[-1]:r[-1]+1])] + ['']*(r[-1]+1 - l[-1] - 1)
            l.pop()
            r.pop()
        elif e in '&|':
            li_element.append(temp)
            temp = ''
            li_element.append(e)
        else:
            temp += e
    li_element.append(temp)    
    return cal_multi_condi_li(li_element)

# main process
def main():
    print('Type part of name to search ACT contact. Type "*help" to get detail instruction. Type "exit" to leave.\nType *cal to enter caculation mode.')
#    global DICT_KEY_CONTACT, DICT_TERM_KEY,  PATH_DICT_KEY_CONTACT, PATH_DICT_TERM_KEY    
    while True:
        str_input = input('\nSeach >>> ')#.lower()
        '''
        if str_input in DICT_TERM_KEY:
            ## matched
            for k in DICT_TERM_KEY[str_input]:
                print('\n', '>'+'\t'.join(DICT_KEY_CONTACT[k]))
        '''
        # add search term function
        if str_input in ['*addterm', '*add1']:
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
        elif str_input in LI_EXIST_WORDS:
            break
        elif str_input in ['hi', 'hello']:
            print('HI')
            #break
        elif str_input in ['*cal', '*c']:
            print('Caculation_mode:')
            while True:
                str_input = input('\nCalculator >>> ')
                if str_input in LI_EXIST_WORDS:
                    break
                else:
                    try:
                        print('answer: ', parse(str_input))
                    except:
                        print('formula error !')
                        pass
        elif str_input in ['*help', '*h']:
            print('\n# Type "*addterm", "*add1" to add search term linked to someone. \n# Type "*addinfo" or "*add2" to add additional info to someone. \n# Type "exit", "ex" to leave.')
        else:
            #raw_match(str_input, DICT_TERM_KEY, DICT_KEY_CONTACT)
            try:
                #set_matches = search(str_input)
                set_matches = parse_formula(str_input)
            except:
                print('formula error !')
                pass
            if not set_matches:
                print(f'\n "{str_input}" not found. Retry or type "exit" to exit.')
            else:
                for r in set_matches:
                    print('\n', '>'+'\t'.join(DICT_KEY_CONTACT[r]))
            



if __name__ == '__main__':
    main()

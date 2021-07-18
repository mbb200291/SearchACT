'''
To lookup the contact info by query the name or other info.
'''

from sys import argv
from os import path
### custom functions
from modules.search import SearchACT
import modules.calculator as cal
from modules.contact import Contact
from modules.help_info import help_

__version__ = '2.0.0'

PATH_OF_SCRIPT = path.dirname(argv[0])
# PATH_DICT_KEY_CONTACT = path.join(PATH_OF_SCRIPT, '_dict_key_contacts.pkl')
# PATH_DICT_TERM_KEY = path.join(PATH_OF_SCRIPT, '_dict_terms_key.pkl')
PATH_DICT_DATA = path.join(PATH_OF_SCRIPT, '_dict_data.pkl')
LI_EXIST_WORDS = ['exit', 'bye', 'ex', 'bye bye', 'quit']


# main process
def main():
    print('Type part of name to search ACT contact. Type "*help" to get detail instruction. Type "exit" to leave.\nType *cal to enter caculation mode.')
    calculator = cal.Calculator(cal.names, cal.ops)
    contact_ = Contact(PATH_DICT_DATA)
    
    # check version
    contact_.check_version()

    while True:
        str_input = input('\nSeach >>> ')#.lower()

        # add search term function
        if str_input in ['*update']:
            contact_.re_build()

        elif str_input in ['*addterm', '*add1']:
            print('into adding mode')
            str_input_KEY = input('Type the E-mail ID (for example, type "benlin" for "benlin@actgenomics.com") or type "exit" to exit. >>> ').lower()
            if str_input_KEY in LI_EXIST_WORDS:
                break
            #elif hash(str_input_KEY) not in contact_.DICT_KEY_CONTACT.keys():
            elif not contact_.key_exist(str_input_KEY):
                print('*** The ID not exist. ***')
                continue
            str_input_Term = input('Type the new search term or type "exit" to exit.\n>>> ').lower()
            if str_input_Term in LI_EXIST_WORDS:
                break
            ans = contact_.add_searchTerm_to_key(str_input_Term, str_input_KEY)
            if ans == 0:
                pass
            else:
                break
        
        # add contact info function
        elif str_input in ['*addinfo', '*add2']:
            str_input_KEY = input('Type the E-mail ID (for example, type "benlin" for "benlin@actgenomics.com") or type "exit" to exit.\n>>> ').lower()
            if str_input_KEY in LI_EXIST_WORDS:
                break
            #elif hash(str_input_KEY) not in contact_.DICH_MAPPING_DATA.keys():
            elif not contact_.key_exist(str_input_KEY):
                print('*** The ID not exist. ***')
                continue
            str_add_info = input('Type the new info of the person or type "exit" to exit.\n>>> ').lower()
            if str_add_info in LI_EXIST_WORDS:
                break
            ans = contact_.add_contactInfo(str_input_KEY, str_add_info)
            if ans == 0:
                pass
            else:
                break
        
        # remove contact info function
        elif str_input in ['*rminfo', '*rm2']:
            pass
            #contact_.rm_ifno()
        elif str_input in ['*rebuild', '*rb']:
            contact_.re_build()
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
                        print('answer: ', str(calculator.cal(str_input)))
                    except:
                        print('formula error !')
                        pass
        elif str_input in ['*help', '*h']:
            print()
            print(f'    version: {__version__}')
            print(f'    contact version: {contact_.DICH_MAPPING_DATA.get("*version")}')
            print(help_())
        elif str_input in ['*version', '*ver']:    
            print()
            print(f'    version: {__version__}')
            print(f'    contact version: {contact_.DICH_MAPPING_DATA.get("*version")}')
        else:
            #raw_match(str_input, DICT_TERM_KEY, DICT_KEY_CONTACT)
            try:
                #set_matches = search(str_input)
                #set_matches = parse_formula(str_input)
                searchact_ = SearchACT(contact_.DICH_MAPPING_DATA)
                set_matches = searchact_.parse_formula(str_input)
            except:
                print('formula error !')
                set_matches = None
                pass
            if not set_matches:
                print(f'\n "{str_input}" not found. Retry or type "exit" to exit.')
            else:
                for r in set_matches:
                    print('\n', '>'+'\t'.join(contact_.DICH_MAPPING_DATA[r]))

if __name__ == '__main__':
    main()

'''
To lookup the contact info by query the name or other info.
'''
from sys import argv
from os import path
from modules.search import SearchACT
import modules.calculator as cal
from modules.contact import Contact
from modules.help_info import help_


__version__ = '2.0.0'
PATH_OF_SCRIPT = path.dirname(argv[0])
PATH_DICT_DATA = path.join(PATH_OF_SCRIPT, '_dict_data.pkl')
LI_EXIST_WORDS = ['exit', 'bye', 'ex', 'quit']


def main():
    print('Type part of name to search ACT contact. Type "*help" to get detail instruction. Type "exit" to leave.\nType *cal to enter caculation mode.')
    calculator = cal.Calculator(cal.names, cal.ops)
    contact = Contact(PATH_DICT_DATA)

    while True:
        str_input = input('\nSeach >>> ')

        # re-build contact dictionary
        if str_input in ['*update']:
            contact.re_build()

        # add search term
        elif str_input in ['*addterm', '*add1']:
            print('into adding mode')
            str_input_key = input('Type the E-mail ID (for example, type "benlin" for "benlin@actgenomics.com") or type "exit" to exit. >>> ').lower()
            if str_input_key in LI_EXIST_WORDS:
                break
            elif not contact.key_exist(str_input_key):
                print('*** The ID not exist. ***')
                continue
            str_input_term = input('Type the new search term or type "exit" to exit.\n>>> ').lower()
            if str_input_term in LI_EXIST_WORDS:
                break
            ans = contact.add_searchTerm_to_key(str_input_term, str_input_key)
            if ans == 0:
                pass
            else:
                break
        
        # add contact info to key
        elif str_input in ['*addinfo', '*add2']:
            str_input_key = input('Type the E-mail ID (for example, type "benlin" for "benlin@actgenomics.com") or type "exit" to exit.\n>>> ').lower()
            if str_input_key in LI_EXIST_WORDS:
                break
            elif not contact.key_exist(str_input_key):
                print('*** The ID not exist. ***')
                continue
            str_add_info = input('Type the new info of the person or type "exit" to exit.\n>>> ').lower()
            if str_add_info in LI_EXIST_WORDS:
                break
            ans = contact.add_contact_info(str_input_key, str_add_info)
            if ans == 0:
                pass
            else:
                break
        
        # remove contact info function
        elif str_input in ['*rminfo', '*rm2']:
            pass
            #contact.rm_ifno()

        # exit 
        elif str_input in LI_EXIST_WORDS:
            break

        # say hello
        elif str_input in ['hi', 'hello']:
            print('HI')

        # calculator
        elif str_input in ['*cal', '*c', "$"]:
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

        # help info
        elif str_input in ['*help', '*h']:
            print()
            print(f'    version: {__version__}')
            print(f'    contact version: {contact.DICT_MAPPING_DATA.get("*version")}')
            print(help_())
        
        # get version info
        elif str_input in ['*version', '*ver']:    
            print()
            print(f'    version: {__version__}')
            print(f'    contact version: {contact.DICT_MAPPING_DATA.get("*version")}')
        else:
            try:
                searchact = SearchACT(contact.DICT_MAPPING_DATA)
                ls_persons = searchact.get_person(str_input)
                if ls_persons:
                    for person in ls_persons:
                        print('\n', '>'+'\t'.join(person))
                else:
                    print(f'\n "{str_input}" not found. Retry or type "exit" to exit.')
            except:
                print('formula error !')
                pass

if __name__ == '__main__':
    main()

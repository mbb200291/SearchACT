
"""
To manage dictionary update operations.

"""
__version__ = 'develop'

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
    
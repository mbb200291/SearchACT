# contact manager
```
PATH_OF_SCRIPT = path.dirname(argv[0]) # get pickle file location
PATH_DICT_DATA = path.join(PATH_OF_SCRIPT, '_dict_data.pkl')
LI_EXIST_WORDS = ['exit', 'bye', 'ex', 'quit']

# initiate
contact_ = Contact(PATH_DICT_DATA) 

# rebuild dictionary from excel
contact_.re_build()

# add search term
contact_.add_searchTerm_to_key(str_input_term, str_input_key)

# add contact information
contact_.add_contact_info(str_input_key, str_add_info)

# remove lookup term (not yet implement)
contact_.rm_term(str_input_term)

# remove person contact info (not yet implement)
contact_.rm_contact(str_input_key)

```

# search controller
```
# initiate (note: should re-initiate if the contact manage had rebuild or add term)
searchact_ = SearchACT(contact_.DICT_MAPPING_DATA) 

# get persons contact
ls_persons = searchact_.get_person(str_input) # list 
```

# calculator usage
```
calculator = cal.Calculator(cal.names, cal.ops)
calculator.cal(str_input)
```
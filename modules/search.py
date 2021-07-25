def index_from_end(li_, match):
    for i in range(len(li_)-1, -1, -1):
        if li_[i] == match:
            return i
    return None


def min_edit_distance(str_target, str_input, cost_ins=1, cost_del=1, cost_sub=2, cost_switch=1):
    '''
    calculate Damerau–Levenshtein distance
    '''
    matrix = [[0 for i in range(len(str_target)+1)] for j in range(len(str_input)+1)]
    for i in range(len(str_target)+1):
        matrix[0][i] = i
    for j in range(len(str_input)+1):
        matrix[j][0] = j
        
    for i in range(1, (len(str_target)+1)):
        for j in range(1, len(str_input)+1):
            if str_target[i-1]==str_input[j-1]:
                cost_sub_ = 0
            else:
                cost_sub_ = cost_sub
            matrix[j][i] = min(
                matrix[j-1][i-1] + cost_sub_, # substitution
                matrix[j][i-1] + cost_del, # delete on input
                matrix[j-1][i] + cost_ins, # insert on input
            )
            if (i>2 and j>2) and str_target[i-1]==str_input[j-2] and str_target[i-2]==str_input[j-1]: # switch on neighbor two nt
                matrix[j][i] = min(
                    matrix[j][i], 
                    matrix[j-2][i-2] + cost_switch
                    )
    return matrix[-1][-1]


class SearchACT():
    def __init__(self, dict_mapping_data):
        self.DICT_MAPPING_DATA = dict_mapping_data

    def search(self, str_input, ed_cutoff=1, min_len=3):
        '''
        Return by the matched keys by str_input.

        '''
        set_match_key = set()
        for term in self.DICT_MAPPING_DATA:
            if not term.startswith('@'): # skip key string
                # string partial matching
                if str_input in term:
                    for key in self.DICT_MAPPING_DATA[term]:
                        set_match_key.add(key)

                # string fuzzy matching
                if (min_edit_distance(term, str_input) <= (ed_cutoff * min(len(term), len(str_input)) // 3)): # cutoff of edit distance will increase when input getting larger
                    for key in self.DICT_MAPPING_DATA[term]:
                        set_match_key.add(key)
        return set_match_key

    def cal_multi_condi_li(self, li_ele):
        #print(li_ele)
        li_ele = [x for x in li_ele if x]
        if len(li_ele)==1 and type(li_ele[0])==str:
            return self.search(li_ele[0])
        elif len(li_ele)==1 and type(li_ele[0])==set:
            return li_ele[0]
        elif len(li_ele)>1 and not [x for x in li_ele if x in ['|', '&']]:
            print('should not exist')
            set_ = set()
            for i in li_ele:
                set_.update(self.search(i))
            return set_
        else:
            for i in [x for x in ['|', '&'] if x in li_ele]:
                #offset = li_ele.index(i)
                offset = index_from_end(li_ele, i)
                left, op, right = li_ele[:offset], li_ele[offset:offset+1], li_ele[offset+1:]
                if op == ['&']:
                    return self.cal_multi_condi_li(left) & self.cal_multi_condi_li(right)
                elif op == ['|']:
                    return self.cal_multi_condi_li(left) | self.cal_multi_condi_li(right)

    def parse_formula(self, s):
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
                li_element[l[-1]:r[-1]+1] = [self.cal_multi_condi_li(li_element[l[-1]:r[-1]+1])] + ['']*(r[-1]+1 - l[-1] - 1)
                l.pop()
                r.pop()
            elif e in '&|':
                li_element.append(temp)
                temp = ''
                li_element.append(e)
            else:
                temp += e
        li_element.append(temp)    
        return self.cal_multi_condi_li(li_element)

    def get_person(self, str_input):
        set_matches = self.parse_formula(str_input)
        return [self.DICT_MAPPING_DATA[r] for r in set_matches]
        # for r in set_matches:
        #     print('\n', '>'+'\t'.join(contact_.DICT_MAPPING_DATA[r]))

        # try:
        #     searchact_ = SearchACT(self.DICT_MAPPING_DATA)
        #     set_matches = searchact_.parse_formula(str_input)
        # except:
        #     print('formula error !')
        #     set_matches = None
        #     pass
        # if not set_matches:
        #     print(f'\n "{str_input}" not found. Retry or type "exit" to exit.')
        # else:
        #     for r in set_matches:
        #         print('\n', '>'+'\t'.join(contact_.DICT_MAPPING_DATA[r]))

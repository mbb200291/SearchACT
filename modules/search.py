def index_from_end(li_, match):
    for i in range(len(li_)-1, -1, -1):
        if li_[i] == match:
            return i
    return None

class SearchACT():
    def __init__(self, di_term_key):
        self.DICT_TERM_KEY = di_term_key

    def search(self, str_input):
        '''
        Return by the matched keys by str_input.

        '''
        set_match_key = set()
        for term in self.DICT_TERM_KEY:
            if str_input in term:
                for key in self.DICT_TERM_KEY[term]:
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

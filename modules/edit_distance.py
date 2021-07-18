'''
return edit-distance match term under given distance.
'''

def min_edit_distance(str_target, str_input, cost_match=0, cost_ins=1, cost_del=1, cost_sub=2, cost_switch=1):
    '''
    calculate Damerau–Levenshtein distance
    '''
    matrix = [[0 for i in range(len(str_target)+1)] for j in range(len(str_input)+1)]
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
            if (i>2 and j>2) and str_target[i-1]==str_input[j-2] and str_target[i-2]==str_input[j-1]:
                matrix[j][i] = min(
                    matrix[j][i], 
                    matrix[j-2][i-2] + cost_switch
                    )
    return matrix[-1][-1]
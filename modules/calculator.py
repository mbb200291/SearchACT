import time

def cal(s,lop):
    s = handle(s)
    if not any(x in s for x in ['+','-','*', '/']):
        return float(s)
    for i in ['+','-','*', '/']:
        left, op, right = s.partition(i)
        # print(i, [left, op, right])
        if op in ['+', '-','*','/']:
            if op == '*':
                if right == '':
                    return(cal(left,lop))
                else:
                    return(cal(left,lop) * cal(right,lop))
            elif op == '/':
                if lop != '/':
                    lop = '/'
                elif lop == '/':
                    return(cal(left,lop) * cal(right,lop))   
                    lop = ''
                return(cal(left,lop) / cal(right,lop))
            elif op == '+':
                if left == '':
                    return(cal('0+'+right,lop))
                else:
                    return(cal(left,lop) + cal(right,lop))
            elif op == '-':
                if left == '':
                    return(cal('0-'+right,lop))
                else:
                    if lop != '-':
                        lop = '-'
                    elif lop == '-':
                        return(cal(left,lop) + cal(right,lop))   
                        lop = ''
                    return(cal(left,lop) - cal(right,lop))

def parse(s, lop=''):
    if s == '':
        return 'Empty string!'
    l = []
    r = []
    s = s.replace(' ','')
    while any(x in s for x in ['(',')']):
        for p in range(len(s)):
            if s[p] == '(' and len(r) < 1:
                l.append(p)
            elif s[p] == ')':
                if len(l) == 0:
                    return('left bracket first!')
                else:
                    r.append(p)
                    if s[l[-1]+1:r[-1]] == '':
                        return 'formula error!'
                    else:
                        ans = cal(s[l[-1]+1:r[-1]],lop)
                    s = "".join((s[:l[-1]],str(ans),s[r[-1]+1:]))
                    l.clear()
                    r.pop()
                    break
    s = handle(s)
    return str(cal(s,lop))

def handle(s):  
    timestart = time.time()
    while any(x in s for x in ['+-','--','*-', '/-']) and time.time() < timestart+5:
        if '+-' in s:
            s=s.replace('+-','-')
        elif '--' in s:
            if s.find('--') == 0:
                s=s.replace('--','')
            s=s.replace('--','+')
        elif '*-' in s:
            p = s.find('*-')
            for i in range(p-1,-1,-1):
                if s[i] in ['+','-','*','/']: 
                    s="".join((s[:i+1],'-',s[i+1:]))
                    s="".join((s[:p+1],'*',s[p+3:]))
                    break
                elif i == 0:
                    s="".join(('-',s[i:]))
                    s="".join((s[:p+1],'*',s[p+3:]))
        elif '/-' in s:
            p = s.find('/-')
            for i in range(p-1,-1,-1):
                if s[i] in ['+','-','*','/']: 
                    s="".join((s[:i+1],'-',s[i+1:]))
                    s="".join((s[:p+1],'/',s[p+3:]))
                    break
                elif i == 0:
                    s="".join(('-',s[i:]))
                    s="".join((s[:p+1],'/',s[p+3:]))
    return(s)

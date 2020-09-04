OPSPECIAL = {
    ' ':'',
    '^-':'np',
    '**-':'np',
    '^':'pp',
    '**':'pp',
    }

def cal(s, lop):
    s = handle(s)
    if 'pp-' in s:
        s = s.replace('pp-','np')
    elif 'np-' in s:
        s = s.replace('np-','pp')
    if not any(x in s for x in ['+', '-', '*', '/']):
        # print(s)
        if any(x in s for x in ['pp', 'np']):
            print(s)
            return specialop(s)
        else:
            return float(s)
    for i in ['+', '-', '*', '/']:
        left, op, right = s.partition(i)
        # print(i, [left, op, right])
        if op in ['+', '-', '*', '/']:
            if op == '*':
                return cal(left,lop) * cal(right,lop)
            elif op == '/':
                if lop == '/':
                    return cal(left, '') * cal(right, '/')
                return cal(left, '') / cal(right, '/')
            elif op == '+':
                if left == '':
                    return cal(f'0+{right}', '')
                else:
                    return cal(left, '') + cal(right, '')
            elif op == '-':
                if left == '':
                    return cal(f'0-{right}', '')
                else:
                    if lop == '-':
                        return cal(left, '') + cal(right, '-')
                    return cal(left, '') - cal(right, '-')

def parse(s):
    if s == '':
        return 'Empty string!'
    if s.count('(') != s.count(')'):
        return 'Formula error!'
    q = -1

    for i in OPSPECIAL.keys():
        s = s.replace(i,OPSPECIAL[i])

    while any(x in s for x in ['(',')']):
        for p in range(len(s)):
            if s[p] == '(':
                q = p
            elif s[p] == ')':
                if q < 0:
                    return 'Left bracket first!'
                else:
                    if s[q+1:p] == '':
                        return 'Formula error!'
                    else:
                        ans = cal(s[q+1:p], '')
                    s = f'{s[:q]}{ans}{s[p+1:]}'
                    q = -1
                    break
    print(s)
    return str(cal(s, ''))

def handle(s):  
    while any(x in s for x in ['+-', '--', '*-', '/-']):
        if '+-' in s:
            s = s.replace('+-', '-')
        elif '--' in s:
            s = s.replace('--', '+')
        elif '*-' in s:
            p = s.find('*-')
            for i in range(p-1, -1, -1):
                if s[i] in ['+', '-', '*', '/']:
                    s = f'{s[:i+1]}-{s[i+1:p]}*{s[p+2:]}'
                    break
                elif i == 0:
                    s = f'-{s[i:p]}*{s[p+2:]}'
        elif '/-' in s:
            p = s.find('/-')
            for i in range(p-1, -1, -1):
                if s[i] in ['+', '-', '*', '/']:
                    s = f'{s[:i+1]}-{s[i+1:p]}/{s[p+2:]}'
                    break
                elif i == 0:
                    s = f'-{s[i:p]}/{s[p+2:]}'
    return s
def specialop(s):
    q = ''
    while any(x in s for x in ['pp','np']):
        for p in range(len(s),-1,-1):
            if s[p-2:p] in ['np','pp'] and q == '':     
                if s.count('pp') + s.count('np') == 1:
                    n = s.find('pp') if s.find('pp') > 0 else s.find('np')
                    # print(s,n)
                    if s[n:n+2] == 'pp':
                        s = f'{float(s[:n])**float(s[n+2:])}'
                    elif s[n:n+2] == 'np':    
                        s = f'{float(s[:n])**-float(s[n+2:])}'
                    break
                else:    
                    q = s[p-2:p]
            elif s[p-2:p] in ['np','pp']:
                n = s.find(q, p)
                if s[n:n+2] == 'pp':
                    ans = float(s[p:n])**float(s[n+2:])
                elif s[n:n+2] == 'np':    
                    ans = float(s[p:n])**-float(s[n+2:])
                s=f'{s[0:p]+str(ans)}'
                # print(p,n,s)
                q=''
                break
    return(float(s))       

if __name__ == '__main__':
    print(parse('2*2**-2*(-2/-2-3+5+5+(6**2)+6**(2-3)-5*6/-2)'))

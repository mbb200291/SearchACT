import time

def cal(s, lop):
    s = handle(s)
    if not any(x in s for x in ['+', '-', '*', '/']):
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
    q = -1
    s = s.replace(' ','')
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

if __name__ == '__main__':
    print(parse('+5+6*((25-9/2)-3*5/85/-12-22*5)-53/-2+(-2/(2+5-3*5*-5))'))

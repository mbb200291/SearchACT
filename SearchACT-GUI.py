import platform
import os
import pickle
import tkinter
import time

runOS = platform.system()

rootPath = os.path.dirname(os.path.abspath(__file__))
dataPath = os.path.join(rootPath, '_dict_key_contacts.pickle')
with open(dataPath, 'rb') as file:
    data = pickle.load(file)
dmapPath = os.path.join(rootPath, '_dict_terms_key.pickle')
with open(dmapPath, 'rb') as file:
    dmap = pickle.load(file)

class SearchACTModel:
    def __init__(self, data, dmap):
        self.data = data
        self.dmap = dmap

    def search(self, text):
        ndata = []
        if text in self.dmap:
            for key in self.dmap[text]:
                ndata.append(data[key])
        else:
            dataMatch = set()
            for kwarg in self.dmap:
                if text in kwarg:
                    for key in self.dmap[kwarg]:
                        dataMatch.add(key)
            for key in dataMatch:
                ndata.append(self.data[key])
        if (len(ndata) == 0):
            return [[f'"{text}" not in list.']]
        else:
            return ndata

    def calculate(self, text):
        try:
            result = eval(text)
            return [[str(result)]]
        except:
            return [['Formula error!']]

class ScrollTable(tkinter.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.data = [['Empty']]
        self.labels = []
        self.canvas = tkinter.Canvas(self)
        self.view = tkinter.Frame(self.canvas)
        self.vsb = tkinter.Scrollbar(self, orient='vertical', command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.vsb.set)
        self.canvas_window = self.canvas.create_window((0, 0), window=self.view, anchor='nw')
        self.canvas.bind('<Configure>', self.onCanvasConfigure)
        self.view.bind('<Configure>', self.onFrameConfigure)
        self.view.bind_all('<Button>', self.onMouseWheel)
        self.view.bind_all('<MouseWheel>', self.onMouseWheel)
        self.vsb.pack(side='right', fill='y')
        self.canvas.pack(fill='both', expand=True)
        self.update()

    def onFrameConfigure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox('all'))

    def onCanvasConfigure(self, event):
        self.canvas.itemconfig(self.canvas_window, width=event.width)

    def onMouseWheel(self, event):
        if event.num == 4 or event.delta > 0:
            self.canvas.yview('scroll', -1, 'units')
        elif event.num == 5 or event.delta < 0:
            self.canvas.yview('scroll', 1, 'units')

    def update(self):
        for label in self.labels:
            label.grid_forget()
        self.labels = []
        for ridx, rdata in enumerate(self.data):
            for cidx, cdata in enumerate(rdata):
                label = tkinter.Label(self.view, text=cdata)
                label.grid(row=ridx, column=cidx, sticky='w')
                self.labels.append(label)

    def setData(self, data):
        self.data = data
        self.update()

class SearchACTView(tkinter.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title('SearchACT')
        self.geometry('800x600')
        self.container = tkinter.Frame(self)
        self.container.pack(fill='both', padx=5, pady=5, expand=True)
        self.inputContainer = tkinter.Frame(self.container)
        self.inputContainer.pack(fill='x')
        self.inputLabel = tkinter.Label(self.inputContainer, text='Input:')
        self.inputText = tkinter.Entry(self.inputContainer)
        self.searchButton = tkinter.Button(self.inputContainer, text='Search')
        self.calculateButton = tkinter.Button(self.inputContainer, text='Calculate')
        self.inputLabel.pack(side='left')
        self.calculateButton.pack(side='right')
        self.searchButton.pack(side='right')
        self.inputText.pack(side='left', fill='x', expand=True)
        self.outputContainer = ScrollTable(self.container)
        self.outputContainer.pack(fill='both', expand=True)

class SearchACTController:
    def __init__(self):
        self.model = SearchACTModel(data, dmap)
        self.view = SearchACTView()
        self.view.searchButton['command'] = self.search
        self.view.calculateButton['command'] = self.calculate
        self.view.mainloop()

    def search(self):
        text = self.view.inputText.get().lower()
        result = self.model.search(text)
        self.view.outputContainer.setData(result)

    def calculate(self):
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


        def parse(s,lop=''):
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
        text = self.view.inputText.get()
        result = self.model.calculate(parse(text))
        self.view.outputContainer.setData(result)

if __name__ == '__main__':
    app = SearchACTController()

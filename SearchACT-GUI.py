import platform
import os
import pickle
import tkinter

runOS = platform.system()

rootPath = os.path.dirname(os.path.abspath(__file__))
dataPath = os.path.join(rootPath, '_dict_key_contacts.pickle')
with open(dataPath, 'rb') as file:
    data = pickle.load(file)
dmapPath = os.path.join(rootPath, '_dict_terms_key.pickle')
with open(dmapPath, 'rb') as file:
    dmap = pickle.load(file)

class Widget(object):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.create()

    def create(self):
        raise NotImplementedError()

    def update(self):
        raise NotImplementedError()

class SearchACT(Widget, tkinter.Tk):
    def __init__(self):
        super().__init__()

    def create(self):
        self.title('SearchACT')
        self.geometry('800x600')
        self.container = RootFrame(self)
        self.container.pack(fill='both', padx=5, pady=5, expand=True)
        self.container.inputContainer.search['command'] = self.search
        self.container.inputContainer.calculate['command'] = self.calculate

    def search(self):
        text = self.container.inputContainer.text.get().lower()
        ndata = []
        if text in dmap:
            for key in dmap[text]:
                ndata.append(data[key])
        else:
            dataMatch = set()
            for kwarg in dmap:
                if text in kwarg:
                    for key in dmap[kwarg]:
                        dataMatch.add(key)
            for key in dataMatch:
                ndata.append(data[key])
        if (len(ndata) == 0):
            self.container.outputContainer.setData([[f'"{text}" not in list.']])
        else:
            self.container.outputContainer.setData(ndata)

    def calculate(self):
        text = self.container.inputContainer.text.get()
        try:
            result = eval(text)
            self.container.outputContainer.setData([[str(result)]])
        except:
            self.container.outputContainer.setData([['Formula error!']])


class RootFrame(Widget, tkinter.Frame):
    def create(self):
        self.inputContainer = InputFrame(self)
        self.outputContainer = OutputFrame(self)
        self.inputContainer.pack(fill='x')
        self.outputContainer.pack(fill='both', expand=True)

class InputFrame(Widget, tkinter.Frame):
    def create(self):
        self.label = tkinter.Label(self, text='Input:')
        self.text = tkinter.Entry(self)
        self.search = tkinter.Button(self, text='Search')
        self.calculate = tkinter.Button(self, text='Calculate')
        self.label.pack(side='left')
        self.calculate.pack(side='right')
        self.search.pack(side='right')
        self.text.pack(side='left', fill='x', expand=True)

class OutputFrame(Widget, tkinter.Frame):
    def __init__(self, *args, **kwargs):
        self.data = [['Empty']]
        self.labels = []
        super().__init__(*args, **kwargs)

    def onFrameConfigure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox('all'))

    def onCanvasConfigure(self, event):
        self.canvas.itemconfig(self.canvas_window, width=event.width)

    def onMouseWheel(self, event):
        if event.num == 4 or event.delta > 0:
            self.canvas.yview('scroll', -1, 'units')
        elif event.num == 5 or event.delta < 0:
            self.canvas.yview('scroll', 1, 'units')

    def create(self):
        self.configure(bg='white')
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


if __name__ == '__main__':
    app = SearchACT()
    app.mainloop()

import platform
import os
import pickle
import tkinter
import modules.calculator
import modules.contact
import modules.search

runOS = platform.system()
rootPath = os.path.dirname(os.path.abspath(__file__))
dataPath = os.path.join(rootPath, '_dict_key_contacts.pickle')
dmapPath = os.path.join(rootPath, '_dict_terms_key.pickle')

class SearchACTModel:
    def __init__(self, contact, searcher, calculator):
        self.contact = contact
        self.searcher = searcher
        self.calculator = calculator

    def search(self, text):
        try:
            matchIDs = self.searcher.parse_formula(text)
            if len(matchIDs) == 0:
                return [[f'\'{str_input}\' not found.']]
            else:
                data = []
                for matchID in matchIDs:
                    data.append(self.contact.DICT_KEY_CONTACT[matchID])
                return data
        except:
            return [['Formula error!']]

    def calculate(self, text):
        try:
            result = self.calculator.cal(text)
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
        cont = modules.contact.Contact(dataPath, dmapPath)
        search = modules.search.SearchACT(cont.DICT_TERM_KEY)
        names = modules.calculator.names
        ops = modules.calculator.ops
        cal = modules.calculator.Calculator(names, ops)
        self.model = SearchACTModel(cont, search, cal)
        self.view = SearchACTView()
        self.view.searchButton['command'] = self.search
        self.view.calculateButton['command'] = self.calculate
        self.view.mainloop()

    def search(self):
        text = self.view.inputText.get().lower()
        result = self.model.search(text)
        self.view.outputContainer.setData(result)

    def calculate(self):
        text = self.view.inputText.get()
        result = self.model.calculate(text)
        self.view.outputContainer.setData(result)

if __name__ == '__main__':
    app = SearchACTController()

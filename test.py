#dict_ = {}
dict_ = 1

def addv():
    #dict_[1] = 1
    global dict_
    dict_ += 1

addv()
print(dict_)
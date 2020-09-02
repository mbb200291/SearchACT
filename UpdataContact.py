'''

version:
- 1.3.0:
 - add phone number query key
- 1.4.0:
 - add department name
 -1.5.1:
 - new rule
 - 1.6.0: update contact by searching contact file("行動基因通訊錄") within same folder of this script
 - 1.7.0: modify some code for other os system

next version:
 - keep customize content

'''


import pandas as pd
from sys import argv
from os import path, listdir
import pickle

__version__ = '1.7.0'

def save_obj_to_pickle(path_, obj): #will end with pickle
    print('# saving file to:', '%s.pickle'%path_)
    with open('%s.pickle'%path_, 'wb') as f_pkl:
        pickle.dump(obj, f_pkl)

def read_pickle(path_):
    with open(path_, 'rb') as file:
        return pickle.load(file)

def locate_contact_file():
    cwd = path.dirname(path.abspath(__file__))
    print(cwd)
    path_contact = sorted([x for x in listdir(cwd) if ".xlsx" in x and not x.startswith('~$')])[-1]
    #print([x for x in os.listdir(cwd) if ".xlsx" in x])
    print('# Read file:', path_contact )
    return path.join(cwd, path_contact)

def remove_blank(tab):
    #First, find NaN entries in first column
    blank_row_bool = tab.iloc[:,4].isna()
    #Next, get index of first NaN entry
    blank_row_index =  [i for i, x in enumerate(blank_row_bool) if x][0]
    #Finally, restrict dataframe to rows before the first NaN entry
    return tab.iloc[:(blank_row_index)]

def read_excel(path_contact):
    if path.isfile(path_contact):
        #contacts = pd.read_excel(path_contact, nrows=nrows)
        contacts = remove_blank(pd.read_excel(path_contact))
        contacts.dropna(how="all", inplace=True)
#        contacts = contacts.loc[(~contacts['信     箱'].isna()) & (contacts['信     箱'].str.contains("@"))]
        return contacts, path.splitext(path_contact)[-1]
    else:
        print('*** Contact file not exist')
        return None

def MakeDict(path_contact):#, _nrows):
    ## Read excel
    contacts, excel_file_name = read_excel(path_contact)
    if type(contacts)!=pd.core.frame.DataFrame:
        return None
    ## Make dictionary
    dict_to_PhoneNum = {} #
    dict_PhoneNum_Info = {'*version':excel_file_name, '*ver':excel_file_name}
    
    DI_Apartment_Abbrev = {
        "執行長室": "CEO", 
        #"技術中心": "", 
        #"營運中心": "", 
        #"Group CFO": "", 
        "研究開發處": "RD", 
        "研究開發部": "RD", 
        #"技術移轉部": "", 
        #"智慧財產部": "", 
        #"商業卓越處": "", 
        #"系統整合部": "", 
        #"產品管理部": "", 
        "生物資訊暨人工智慧處": "BI", 
        "生物資訊部": "BI", 
        "人工智慧部": "AI", 
        "數據分析部": "DA", 
        #"資料科學處": "", 
        #"分子檢驗處": "", 
        "次世代定序部": "NGS", 
        #"轉譯醫學處": "", 
        "癌症基因體部": "", 
        #"專案管理部": "", 
        "醫藥資訊部": "MI", 
        #"臨床醫學部": "", 
        "品保與環境監控部": "QA", 
        "法規事務處": "RA", 
        #"銷售業務處": "", 
        #"銷售業務部": "", 
        #"業務行政部": "", 
        #"臨床衛教部": "", 
        #"行政資源處": "", 
        #"行政資源部": "", 
        #"會計處": "", 
        #"財務與出納部": "", 
        "事業暨企業發展處": "BD", 
        "資訊處": "IT", 
        "人力資源處": "HR", 
    }
    for i,R in contacts.iterrows():

        ChnName = R.姓名.strip()
        EngName = str(R['英 文 名']).strip()
        EngName_dd = EngName.replace('-', ' ').strip()
        EngName_dd2 = EngName.replace('-', '').strip()
        MailAress = R['信     箱'].strip()
        PhoneNum = R.分機
        CellPhone = R['手   機']
        Department = R['部門名稱'].strip()
        
        print(ChnName, EngName)
        
        KEY = MailAress.split('@')[0]

        ## first part: key to result
        dict_PhoneNum_Info[KEY] = [str(x) for x in [ChnName, EngName, Department, MailAress, PhoneNum, CellPhone]]

        ## second part: query items to key
        dict_to_PhoneNum.setdefault(ChnName, set()).add(KEY)
        dict_to_PhoneNum.setdefault(ChnName[:-1], set()).add(KEY)
        dict_to_PhoneNum.setdefault(ChnName[-1], set()).add(KEY)
        dict_to_PhoneNum.setdefault(EngName.lower(), set()).add(KEY)
        dict_to_PhoneNum.setdefault(EngName_dd.lower(), set()).add(KEY)
        dict_to_PhoneNum.setdefault(EngName_dd2.lower(), set()).add(KEY)
        dict_to_PhoneNum.setdefault(''.join([x[0].upper() for x in EngName.split(' ')]), set()).add(KEY)
        dict_to_PhoneNum.setdefault(''.join([x[0].upper() for x in EngName_dd.split(' ')]), set()).add(KEY)
        dict_to_PhoneNum.setdefault(''.join([x[0].upper() for x in EngName_dd2.split(' ')]), set()).add(KEY)

        dict_to_PhoneNum.setdefault(EngName[-1].upper()+''.join([x[0].upper() for x in EngName.split(' ')[:-1]]), set()).add(KEY)
        dict_to_PhoneNum.setdefault(EngName[-1].upper()+''.join([x[0].upper() for x in EngName_dd.split(' ')[:-1]]), set()).add(KEY)
        dict_to_PhoneNum.setdefault(EngName[-1].upper()+''.join([x[0].upper() for x in EngName_dd2.split(' ')[:-1]]), set()).add(KEY)

        """
        dict_to_PhoneNum.setdefault(ChnName, set()).add(KEY)
        dict_to_PhoneNum.setdefault(ChnName[1:], set()).add(KEY)
        dict_to_PhoneNum.setdefault(ChnName[:-1], set()).add(KEY)
        dict_to_PhoneNum.setdefault(ChnName[0], set()).add(KEY)
        #
        dict_to_PhoneNum.setdefault(EngName.lower(), set()).add(KEY)
        dict_to_PhoneNum.setdefault(' '.join(EngName.lower().split(' ')[:-1]), set()).add(KEY)
        dict_to_PhoneNum.setdefault(EngName.split(' ')[-1].lower(), set()).add(KEY)
        for i in range(len(EngName.split(' '))):
            dict_to_PhoneNum.setdefault(EngName.split(' ')[i].lower(), set()).add(KEY)
        for i in range(len(EngName.split('-'))):
            dict_to_PhoneNum.setdefault(EngName.split('-')[i].lower(), set()).add(KEY)
        dict_to_PhoneNum.setdefault(EngName_dd.lower(), set()).add(KEY)
        dict_to_PhoneNum.setdefault(' '.join(EngName_dd.lower().split(' ')[:-1]), set()).add(KEY)
        dict_to_PhoneNum.setdefault(EngName_dd.split(' ')[-1].lower(), set()).add(KEY)
        dict_to_PhoneNum.setdefault(EngName_dd2.lower(), set()).add(KEY)
        dict_to_PhoneNum.setdefault(' '.join(EngName_dd2.lower().split(' ')[:-1]), set()).add(KEY)
        dict_to_PhoneNum.setdefault(EngName_dd2.split(' ')[-1].lower(), set()).add(KEY)
        dict_to_PhoneNum.setdefault(''.join(EngName.lower().split(' ')[:-1]), set()).add(KEY)
        dict_to_PhoneNum.setdefault(EngName_dd2[:1].lower(), set()).add(KEY)
        dict_to_PhoneNum.setdefault(EngName_dd2[:2].lower(), set()).add(KEY)
        dict_to_PhoneNum.setdefault(EngName_dd2[:3].lower(), set()).add(KEY)
        dict_to_PhoneNum.setdefault(EngName_dd2[:4].lower(), set()).add(KEY)
        dict_to_PhoneNum.setdefault(EngName_dd2[:5].lower(), set()).add(KEY)
        """
        #
        dict_to_PhoneNum.setdefault(MailAress.split('@')[0].lower(), set()).add(KEY)
        # by Phone num
        dict_to_PhoneNum.setdefault(str(PhoneNum), set()).add(KEY)
        # by cell phone num
        dict_to_PhoneNum.setdefault(str(CellPhone), set()).add(KEY)
        # by department
        dict_to_PhoneNum.setdefault(str(Department), set()).add(KEY)
        ## by department's abbreviation
        dict_to_PhoneNum.setdefault(DI_Apartment_Abbrev.get(str(Department), str(Department)), set()).add(KEY)


    #print(os.path.split(sys.path[0])[0])
    path_term_key = path.join(path.dirname(path_contact), '_dict_terms_key')
    path_key_contact = path.join(path.dirname(path_contact), '_dict_key_contacts')
    save_obj_to_pickle(path_term_key, dict_to_PhoneNum)
    save_obj_to_pickle(path_key_contact, dict_PhoneNum_Info)
    '''
    if regenerate_dict:
        save_obj_to_pickle(path_term_key, dict_to_PhoneNum)
        save_obj_to_pickle(path_key_contact, dict_PhoneNum_Info)
    else:
        save_obj_to_pickle(path_term_key, read_pickle(path_term_key).update(dict_to_PhoneNum))
        save_obj_to_pickle(path_key_contact, read_pickle(path_key_contact).update(dict_PhoneNum_Info))
    '''


def main():
    print('# Loading')
    MakeDict(locate_contact_file())# int(sys.argv[2]))

if __name__ == '__main__':
    main()

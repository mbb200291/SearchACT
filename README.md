# SearchACT
This is a quick tool to search contacts in ACT genomics.

## Copy latest contact file into current directory

```
\\tp-fs01\Public\公司通訊錄及座位表
```

## quick use
```
python SearchACT.py # enter the interactive window

>>> benlin  # serch "benlin" in contact

>林邦齊        Ben Lin 人工智慧部      ******@*******.***  1624    ****-***-***

>>> AI & ben  # multiple condtion to search

>林邦齊        Ben Lin 人工智慧部      ******@*******.***  1624    ****-***-***

>>> (AI & ben) | bruce  # multiple condtion can using bracket to seperate
 
>林邦齊        Ben Lin 人工智慧部      ******@*******.***  1624    ****-***-***

>陳柏劭        Bruce Chen      次世代定序部    ******@*******.***  1520    ****-***-***

>>> *cal    # entering calculator mode
Calculator >>> 1+1*2
answer:  3.0
Calculator >>> exit

>>> ex  # type "ex" to leave
```

## update dictionary
```
python UpdataContact.py
```

## compile as .exe on windows (recommend)
```
pyinstaller -F SearchACT.py -i icon.ico
pyinstaller -F UpdataContact.py
pyinstaller -F SearchACT-GUI.py
```

## install requirements by pip
```
pip install -r requirements.txt
```


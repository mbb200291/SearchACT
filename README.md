# SearchACT
This is a quick tool to search contacts in ACT genomics.

## Put contact file into directory

```
\\tp-fs01\Public\公司通訊錄及座位表
```

## quick use
```
python SearchACT.py # enter the interactive window

>>> benlin  # serch "benlin" in contact

>林邦齊        Ben Lin 人工智慧部      benlin@actgenomics.com  1624    0910-216-4

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
```

## install requirements by pip
```
pip install -r requirements.txt
```

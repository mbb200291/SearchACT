# SearchACT
This is a quick tool to search contacts in ACT genomics.

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

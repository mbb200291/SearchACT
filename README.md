# SearchACT

This is a quick tool to search contacts in ACT genomics.

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

>>> bne   # allow fuzzy search

 >林邦齊        Ben Lin 人工智慧部      ******@*******.***  1624    ****-***-***

>>> *cal    # entering calculator mode
Calculator >>> 1+1*2
answer:  3.0
Calculator >>> exit

>>> ex  # type "ex" to leave
```

## install procedure

### install requirements by pip

```
pip install -r wheelhouse/requirements.txt --no-index --find-links wheelhouse
```

### copy latest contact file to directory of *SearchACT*.

```
\\tp-fs01\Public\公司通訊錄及座位表\<latest file>.xlsx
```

### run

```
python SearchACT.py
```

### or using GUI version

```
python SearchACT-GUI.py
```

### compile as .exe on windows (recommend)

```
pyinstaller -D SearchACT.py -i icon.ico 
pyinstaller -D SearchACT-GUI.py -i icon.ico 

# if compiled exe lacking of `mkl_intel_thread.1.dll`, modify as below (have to manually find the dll file location)
pyinstaller -D .\SearchACT.py -i icon.ico --add-binary 'mkl_intel_thread.1.dll;.'
pyinstaller -D .\SearchACT-GUI.py -i icon.ico --add-binary 'mkl_intel_thread.1.dll;.'
```

### update dictionary 
When programe inititate, it will check the version of excel file. Once get newest excel file, it will automatically update pickle data. However, you still can use this command to update dictionary manually in iteractive window.

```
python SearchACT.py
>>> *update
```

## ready-to-use .exe file 
This File can obtatin from tp-fs01\PUBLIC folder. Directly copy whole folder or just creating symbolic link to your local.

```
\\tp-fs01\Public\SearchACT
```

# GUI for SearchACT

## Start

```
python SearchACT-GUI.py # enter the interactive window
```

## Functions

- Input text field: input some text
- Search button: serch the input text in contact
- Calculate button: calculate the input expression
- File menu
  - Update: rebuild the pickle file from an excel
- Info menu: show version information

## Keyboard shortcuts

- Text + `Enter`: saerch the input text in contact
- Text + `Ctrl` + `Enter`: calculate the input expression
- `Ctrl` + `A`/`a`: select all text in the input text field
- `Ctrl` + `L`/`l`: rebuild the pickle file
- `Ctrl` + `I`/`i`: show version information
- Subwindow + `Esc`: close the subwindow
- Main window + Double `Esc`: exit GUI

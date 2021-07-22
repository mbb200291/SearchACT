# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['SearchACT-GUI.py'],
             pathex=['D:\\ben\\SearchACT'],
             binaries=[('C:\\Users\\mbb20\\anaconda3\\pkgs\\mkl-2021.2.0-haa95532_296\\Library\\bin\\mkl_intel_thread.1.dll', '.')],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name='SearchACT-GUI',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=True , icon='icon.ico')
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               upx_exclude=[],
               name='SearchACT-GUI')

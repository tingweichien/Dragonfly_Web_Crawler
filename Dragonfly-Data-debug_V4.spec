# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['src\\GUI_split.py'],
             pathex=['D:\\Code\\python\\web\\Web_Crawler\\DragonflyData'],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=['hooks'],
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
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='Dragonfly-Data-debug_V4',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=True , icon='docs\\image\\dragonfly_ico.ico')

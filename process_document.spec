# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['C:\\Users\\966\\Projects\\GuangZhiAssistant-main\\apps\\views\\_nicegui\\components\\process_document.py'],
    pathex=[],
    binaries=[],
    datas=[('.', 'nicegui'), ('C:\\Users\\966\\Projects\\GuangZhiAssistant-main\\models\\Lite-Mistral-150M-v2-Instruct-Q4_K_S.gguf', 'models')],
    hiddenimports=['nicegui', 'asyncio'],
    hookspath=['C:\\Users\\966\\Projects\\GuangZhiAssistant-main\\hooks'],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='process_document',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='process_document',
)

# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['src\\winadmin_service.py'],
    pathex=['src'],  # Paths to search for scripts/modules
    binaries=[],  # Any additional binary files you need to include
    datas=[('config/settings.ini', 'config')],  # Include the settings.ini file
    hiddenimports=[
        'win32timezone', 
        'win32service', 
        'win32serviceutil', 
        'win32event'
    ],
    hookspath=[],  # You can leave this empty unless you have custom hooks
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],  # If there are modules you explicitly want to exclude
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,  # Archive the packages into a single file inside the executable
)

pyz = PYZ(
    a.pure,
    a.zipped_data,
    cipher=block_cipher,
)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='WinAdminService',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,  # Use UPX to compress the executable
    upx_exclude=[],  # Exclude any specific files from UPX compression if needed
    runtime_tmpdir=None,
    console=False,  # Set to False to disable console window (True if you want to see logs in console)
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None  # Add an icon file if you want a custom icon for the executable
)

coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='WinAdminService'
)

# packaging/aifx_player_version.py

VSVersionInfo(
  ffi=FixedFileInfo(
    filevers=(0,3,0,0),
    prodvers=(0,3,0,0),
    mask=0x3f,
    flags=0x0,
    OS=0x4,
    fileType=0x1,
    subtype=0x0,
    date=(0,0)
  ),
  kids=[
    StringFileInfo([
      StringTable(
        '040904B0',
        [
          StringStruct('CompanyName', 'AI-First-Exchange'),
          StringStruct('FileDescription', 'AIFX Player'),
          StringStruct('FileVersion', '0.3.0'),
          StringStruct('InternalName', 'AIFX Player'),
          StringStruct('OriginalFilename', 'AIFX Player.exe'),
          StringStruct('ProductName', 'AIFX Player'),
          StringStruct('ProductVersion', '0.3.0')
        ])
    ]),
    VarFileInfo([VarStruct('Translation', [1033, 1200])])
  ]
)
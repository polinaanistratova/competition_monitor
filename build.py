import PyInstaller.__main__
import os

PyInstaller.__main__.run([
    'ui/app.py',
    '--name=competitionmonitor',
    '--onefile',
    '--windowed',
    '--add-data=data:data',
    '--add-data=.env.example:.',
    '--icon=NONE',
])

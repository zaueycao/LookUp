"""
This is a setup.py script generated by py2applet

Usage:
    python setup.py py2app
"""

from setuptools import setup

APP = ['LookUp.py']
APP_NAME = "LookUp"
DATA_FILES = []
OPTIONS = {
    'iconfile':'icon.icns',
    'plist': {
        'CFBundleName': APP_NAME,
        'CFBundleDisplayName': APP_NAME,
        'CFBundleGetInfoString': "Looking for primers",
        'CFBundleIdentifier': "com.zoeycao.osx.lookup",
        'CFBundleVersion': "0.1.0",
        'CFBundleShortVersionString': "0.1.0",
        'NSHumanReadableCopyright': u"Copyright © 2021, Zoey Cao, All Rights Reserved"
    }
}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)

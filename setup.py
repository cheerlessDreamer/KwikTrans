from setuptools import setup

# To build a new application, run: python setup.py py2app

APP = ['kwiktrans.py']
DATA_FILES = [('', ['icon.png'])]
OPTIONS = {
    'argv_emulation': True,
    'iconfile': 'icon.icns',
    'plist': {
        'CFBundleShortVersionString': '0.5.0',
        'LSUIElement': True,
    },
    'packages': ['rumps'],
}

setup(
    app=APP,
    name='KwikTrans',
    author='Danny Taylor',
    author_email='danny@dannytaylor.se',
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
    install_requires=['rumps']
)

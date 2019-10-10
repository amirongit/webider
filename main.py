from libs import stringLib, ormLib
from json import dump, load
from requests import get

cfg = load(open('cfg/settings.json'))

def setup():
    pass

def main():
    pass

if cfg['first_run'] == True:
    setup()

if __name__ == 'main':
    main()

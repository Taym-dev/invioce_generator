import json
import requests
from os import listdir
from os.path import isfile, join


onlyfiles = [f for f in listdir('/Users/a../Documents/school/code/TayTib/test_set_softwareleverancier') if isfile(join('/Users/a../Documents/school/code/TayTib/test_set_softwareleverancier', f))]

for file in onlyfiles:    
    file = open(f'/Users/a../Documents/school/code/TayTib/test_set_softwareleverancier/{file}')
    pipi = json.load(file)
    print(pipi)
import os 
from functools import reduce
import hashlib
import warnings
import re 

CHECK_DIRS = ['./01.working', './02.labeled', './03.verified']
LABELED_DIRS = ['./02.labeled', './03.verified']
MATCH_SKIP_FILES = ['.gitkeep']
EXPECTED_TOTAL_PNG_COUNT = 5002


def get_png_count(dirname) -> int:
    acc = 0
    for _,_,files in os.walk(dirname):
        acc += len(list(filter(lambda x: x.endswith('.png'), files)))
    return acc

def get_file_hash(filepath) -> str: 
    data = None 
    with open(filepath, 'rb') as f: 
        data = f.read()
    if data == None: 
        warnings.warn(f'get_file_hash failed on {filepath}, data cannot be None')
        return None
    return f'{hashlib.md5(data).hexdigest()}:{hashlib.sha256(data).hexdigest()}'
        
def test_total_png_count(): 
    total_png_count = reduce(lambda x, y: x + y, map(get_png_count,  CHECK_DIRS), 0)    
    assert(total_png_count == EXPECTED_TOTAL_PNG_COUNT)

def test_dup_files():
    dupdict = {}  
    dup = False
    for _dirname in CHECK_DIRS:
        for dirpath,_,filenames in os.walk(_dirname):
            for filename in filenames:
                filepath = os.path.join(dirpath, filename)
                hx = get_file_hash(filepath)
                if hx == None: continue
                if hx in dupdict:
                    warnings.warn(f'filehash {hx} is duplicated, hash conflict in `{dupdict[hx]}` and `{filepath}`')
                    dup = True
                else:
                    dupdict[hx] = filepath
    assert(dup == False)

def test_label_naming_rule():
    for labeled_dir in LABELED_DIRS:
        files = os.listdir(labeled_dir)
        for file in files:
            if file in MATCH_SKIP_FILES: continue
            assert(file.endswith('.png'))
            assert(1 < len(file.split('.')) <= 3)
            
            label = file.split('.')[0]
            assert(re.match(r'^[0-9]{4}$', label) != None)
import os.path as op
import tarfile
from urllib.request import urlretrieve

# Updated URL for this mirror
URL_VOC = ("https://github.com/alexwolson/pascal-voc-2007-mirror/"
           "releases/download/latest/VOCtrainval_06-Nov-2007.tar.gz")
FILE_VOC = "VOCtrainval_06-Nov-2007.tar.gz"
FOLDER_VOC = "VOCdevkit"

if not op.exists(FILE_VOC):
    print(f'Downloading from {URL_VOC} to {FILE_VOC}...')
    urlretrieve(URL_VOC, './' + FILE_VOC)

if not op.exists(FOLDER_VOC):
    print(f'Extracting {FILE_VOC}...')
    with tarfile.open(FILE_VOC) as tar:
        tar.extractall()
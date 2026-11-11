import sys
from PIL import Image
from mock import run
run(sys.argv[1],sys.argv[2],[(236,262,140),(627,262,140),(1024,350,160)],Image.open(sys.argv[3]).convert('RGBA'))

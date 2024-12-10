import sys
from PIL import Image
import os
from real_webp import RealWebP

#TODO: use a real argv parser
if len(sys.argv)<3:
    print("put in two filenames bozo (in and out files)")
    exit(1)

in_file = sys.argv[1]
out_file = sys.argv[2]
rwp = RealWebP(0,0)

#TODO: make this better
if in_file.split(".")[-1]=="rwp": # Convert from RWP to other
    rwp.load(in_file)
    rwp.save_to_img(out_file)
else: # Convert from other to RWP
    rwp.load_from_img(in_file)
    rwp.save(out_file)


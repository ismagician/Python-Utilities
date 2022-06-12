import os
import glob, sys
from datetime import date
from subprocess import Popen
import re

def sortKeyFunc(s):

    return int(os.path.basename(s)[:-size])



if len(sys.argv) == 3:
    formato = "."+sys.argv[1]
    video = sys.argv[2]

    size=formato.__len__()

else:
    
    print("Use: python JoinFile.py [input files extension] [output file name]")
    os._exit(0)



myList=list(glob.glob('*'+formato))
myList.sort(key=sortKeyFunc)

# File list ceation
archivo="join.txt"
if os.path.isfile(archivo):
    print("Exists")
    os.unlink(archivo)
    file = open(archivo, 'a')
else:
    file=open(archivo,'a')

for i in range(0,myList.__len__()):
    file.write("file " + myList[i]+"\n")


file.close()


today =str(date.today())

os.system("ffmpeg -f concat -i " + archivo+" -c copy "+ video+"-"+today+formato)

print("Finish")




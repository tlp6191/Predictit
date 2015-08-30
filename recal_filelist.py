#!/usr/bin/python
from bs4 import BeautifulSoup
import re,sqlite3,sys,glob

if len(sys.argv)>1:
  date=sys.argv[1]
else:
  date="SatAug2910:49:59CDT2015"
dir="data-"+date
validcont=[]
with open(dir+"/valid","r") as myfile:
  datafile=myfile
  p=re.compile(".*SingleOption.*=(\d+)")
  for line in datafile:
    m=p.match(line)
#    print "https://www.predictit.org/home/SingleOption?contractID="+str(m.group(1))
    validcont.append(int(m.group(1)))

for i in sorted(validcont):
    print "https://www.predictit.org/home/SingleOption?contractID="+str(i)
maxcont=sorted(validcont)[-1]
for i in range (maxcont+1,maxcont+6):
    print "https://www.predictit.org/home/SingleOption?contractID="+str(i)

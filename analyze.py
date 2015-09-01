#!/usr/bin/python
from bs4 import BeautifulSoup
import re,sqlite3,sys,glob
con=sqlite3.connect(sys.argv[1]+"/contracts.db")
cur=con.cursor()

#Parse through for zero-sum stocks
cur.execute("select sym from contracts")
syms=cur.fetchall()
zsum={}
for sym in syms:
  mark= ".".join(str(sym[0]).split('.')[1:])
  if mark not in zsum:
    zsum[mark]=[str(sym[0])]
  else:
    zsum[mark].append(str(sym[0]))
print zsum
#for key in zsum:
#  if len(zsum[key])>1:
    
  

con.commit()
con.close()

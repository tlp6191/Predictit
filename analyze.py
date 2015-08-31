#!/usr/bin/python
from bs4 import BeautifulSoup
import re,sqlite3,sys,glob
con=sqlite3.connect(sys.argv[1]+"/contracts.db")
cur=con.cursor()

#Parse through for zero-sum stocks
cur.execute("select sym from contracts")
syms=cur.fetchall()

con.commit()
con.close()

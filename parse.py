#!/usr/bin/python
from bs4 import BeautifulSoup
import re,sqlite3,sys,glob
con=sqlite3.connect("contracts.db")
cur=con.cursor()
cur.execute("create table if not exists contracts (id integer primary key autoincrement,sym varchar unique, start, end)")
cur.execute("create table if not exists contract_data (id INTEGER primary key autoincrement,sym_id INTEGER,date INTEGER,traded INTEGER,volume INTEGER,total_shares INTEGER,todays_change REAL)")
cur.execute("create table if not exists offers (id INTEGER primary key autoincrement,sym_id INTEGER,date INTEGER,price INTEGER,count INTEGER,yes NUMBERIC, buy NUMBERIC)")#The yes column is 1 for yes offers, 0 for no offers. Same for buy

if len(sys.argv)>1:
  date=sys.argv[1]
else:
  date="SatAug2910:49:59CDT2015"
dir="data-"+date
for file in glob.glob(dir+"/SingleOption*"):
  try:
    with open(file,"r") as myfile:
      datafile=myfile.read()
    print datafile
    
    soup=BeautifulSoup(datafile,'lxml')
    print soup
    sym=soup.find('td',text=re.compile("Symbol:")).next_sibling.next_sibling.string
    start=soup.find('td',text=re.compile("Start Date:")).next_sibling.next_sibling.string
    end=soup.find('td',text=re.compile("End Date:")).next_sibling.next_sibling.string
    traded=soup.find('td',text=re.compile("Shares Traded:")).next_sibling.next_sibling.string
    volume=soup.find('td',text=re.compile("Today's Volume:")).next_sibling.next_sibling.string
    total_shares=soup.find('td',text=re.compile("Total Shares:")).next_sibling.next_sibling.string
    todays_change=soup.find('td',text=re.compile("Today's Change:")).next_sibling.next_sibling.string
    if todays_change=='NC':
      todays_change=0.0
    print sym,date,start,end,traded,volume,total_shares,todays_change
    cur.execute("SELECT id FROM contracts WHERE sym=(?)",(sym,))
    data=cur.fetchall()
    print data
    if len(data)==0:
      cur.execute("insert into contracts(sym,start,end) values (?, ?, ?)",(sym,start,end))
      contractid=cur.lastrowid
    else: 
      contractid=data[0][0]
    print contractid
    cur.execute("select * from contracts")
    print cur.fetchone()
    cur.execute("insert into contract_data(sym_id,date,traded,volume,total_shares,todays_change) values (?, ?, ?, ?, ?,?)",(contractid,date,traded,volume,total_shares,todays_change))
    try:
      yes=soup.find('th',text=re.compile("Buy Yes")).parent.parent.parent.find("tbody").find_all('span')
      (bprice,sprice)=(int(yes[0].previous_sibling),int(yes[1].previous_sibling))
      for tag in yes:
        price=int(tag.previous_sibling)
        amount=int(tag.parent.next_sibling.next_sibling.string)
        yes=1
        if price>=bprice:
          buy=1
        else:
          buy=0
        cur.execute("insert into offers(sym_id,date,price,count,yes,buy) values (?, ?, ?, ?, ?, ?)",(contractid,date,price,amount,yes,buy))
      no=soup.find('th',text=re.compile("Buy No")).parent.parent.parent.find("tbody").find_all('span')
      (bprice,sprice)=(int(no[0].previous_sibling),int(no[1].previous_sibling))
      for tag in no:
        price=int(tag.previous_sibling)
        amount=int(tag.parent.next_sibling.next_sibling.string)
        yes=0
        if price>=bprice:
          buy=1
        else:
          buy=0
        cur.execute("insert into offers(sym_id,date,price,count,yes,buy) values (?, ?, ?, ?, ?, ?)",(contractid,date,price,amount,yes,buy))
    except:
      print "Symbol "+sym+" seems not to be trading"
  except:
    print "File "+str(file)+" seems to have no usable stock data. Maybe we needed to filter it?"
con.commit()
con.close()

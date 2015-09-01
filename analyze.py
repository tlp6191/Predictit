#!/usr/bin/python
tax_rate=0.1
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
buy_yes={}
buy_no={}
sell_yes={}
sell_no={}
buy_yes_c={}
buy_no_c={}
sell_yes_c={}
sell_no_c={}
#for key in zsum:
cur.execute("select contracts.sym,max(offers.price),contracts.*,offers.* from offers join contracts on offers.sym_id=contracts.id where not exists (select 1 from offers as offers2 where offers2.id=offers.id and offers2.date > offers.date) and offers.yes=1 and offers.buy=1 group by sym_id order by sym_id")
buy_yes_db=cur.fetchall()
cur.execute("select contracts.sym,min(offers.price),contracts.*,offers.* from offers join contracts on offers.sym_id=contracts.id where not exists (select 1 from offers as offers2 where offers2.id=offers.id and offers2.date > offers.date) and offers.yes=1 and offers.buy=0 group by sym_id order by sym_id")
sell_yes_db=cur.fetchall()
cur.execute("select contracts.sym,max(offers.price),contracts.*,offers.* from offers join contracts on offers.sym_id=contracts.id where not exists (select 1 from offers as offers2 where offers2.id=offers.id and offers2.date > offers.date) and offers.yes=0 and offers.buy=1 group by sym_id order by sym_id")
buy_no_db=cur.fetchall()
cur.execute("select contracts.sym,min(offers.price),contracts.*,offers.* from offers join contracts on offers.sym_id=contracts.id where not exists (select 1 from offers as offers2 where offers2.id=offers.id and offers2.date > offers.date) and offers.yes=0 and offers.buy=0 group by sym_id order by sym_id")
sell_no_db=cur.fetchall()
for line in buy_yes_db:
  sym=  str(line[0])
  buy_yes[sym]=int(line[1])
  buy_yes_c[sym]=int(line[2])
for line in buy_no_db:
  sym=  str(line[0])
  buy_no[sym]=int(line[1])
  buy_no_c[sym]=int(line[2])
for line in sell_yes_db:
  sym=  str(line[0])
  sell_yes[sym]=int(line[1])
  sell_yes_c[sym]=int(line[2])
for line in sell_no_db:
  sym=  str(line[0])
  sell_no[sym]=int(line[1])
  sell_no_c[sym]=int(line[2])
for key in buy_yes:
  if buy_yes[key]+buy_no[key]<100:
    print "Guaranteed profit of "+str((100-buy_yes[key]-buy_no[key])*(1.0-tax_rate))
  

con.commit()
con.close()
print "Buy yes="+str(buy_yes)
print "Sell yes="+str(sell_yes)
print "Buy no="+str(buy_no)
print "Sell no="+str(sell_no)

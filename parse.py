#!/usr/bin/python
from bs4 import BeautifulSoup
import re
dir="data-SatAug2910:49:59CDT2015"
file="SingleOption?contractID=526"
with open(dir+"/"+file,"r") as myfile:
  data=myfile.read()
print data
soup=BeautifulSoup(data,'lxml')
print soup
sym=soup.find('td',text=re.compile("Symbol:")).next_sibling.next_sibling.string
start=soup.find('td',text=re.compile("Start Date:")).next_sibling.next_sibling.string
end=soup.find('td',text=re.compile("End Date:")).next_sibling.next_sibling.string
traded=soup.find('td',text=re.compile("Shares Traded:")).next_sibling.next_sibling.string
volume=soup.find('td',text=re.compile("Today's Volume:")).next_sibling.next_sibling.string
total_shares=soup.find('td',text=re.compile("Total Shares:")).next_sibling.next_sibling.string
todays_change=soup.find('td',text=re.compile("Today's Change:")).next_sibling.next_sibling.string
print sym,start,end,traded,volume,total_shares,todays_change

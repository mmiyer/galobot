'''Base of galobot
starts up and logs in
traces stack to get name of calling filename to figure out shutoff
creates "p" object, which is pywikibot with:
an additional function of p.Page, p.Page().savewithshutoff, which gives the ability to save with a check to shutoff
'''

import sys
import pathlib
import time
from traceback import extract_stack
import pywikibot as p

site = p.Site()
site.login()
if not site.logged_in(): print("Not logged in?"); sys.exit()

for x in extract_stack():#trace the stack to get filename, which is the taskname for shutoff
    if not x[0].startswith('<frozen') and not x[0].startswith('pwb'):#find the first filename that could be our taskname
        taskname = pathlib.PurePath(x[0]).stem #get from a path of ".galobot/foo.py" to "foo"
        break

print(taskname)

class Page (p.Page):
    def savewithshutoff (self, shutoff = taskname, **kwargs):
        shutofftitle = "User:Galobot/shutoff/" + shutoff
        spage = p.Page(site, shutofftitle)
        if spage.get() != "":
            print("Bot shutoffed")
            for x in range(1,10):
                time.sleep(60)
                print("Checking shutoff...")
                if spage.get(force = True) == "":
                    print("No longer shutoffed")
                    break
            else:
                print("After checking 10 times still shutoffed, so ending process.")
                sys.exit()
        self.save(**kwargs) #edit page

p.Page = Page

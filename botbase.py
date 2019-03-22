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

def checkshutoff(shutoff):
    shutofftitle = "User:Galobot/shutoff/" + shutoff
    print(shutofftitle)
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
    
class Page (p.Page):
    def savewithshutoff (self, shutoff = taskname, max_edits = False, dry = False, **kwargs):
        checkshutoff(shutoff)
        if max_edits:
            editfilename = shutoff+".txt"
            try:
                with open(editfilename, "r+") as editfile:
                    text = editfile.read()
                    edit_count = int(text)
                    if edit_count >= max_edits:
                        sys.exit("Exiting {} as completed {} edits.".format(taskname, max_edits))
                    else:
                        editfile.seek(0)
                        editfile.write(str(edit_count + 1))
            except FileNotFoundError:
                with open(editfilename, "w") as editfilew:
                    editfilew.write("0")
        if dry:
            print('Page "{}" saved'.format(self.title()))
        else:
            self.save(**kwargs) #edit page

p.Page = Page

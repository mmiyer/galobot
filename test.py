'''
Used to e.g. test whether botbase.py functions properly
'''
from botbase import *

title = "User:Galobot/sandbox"
page = p.Page(site,  title)
page.text += "test"
page.savewithshutoff(summary = "testing, testing, testing", minor = False)

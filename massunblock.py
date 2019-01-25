from botbase import *

with open("unblocklist.txt") as unblocklistfile:
    unblocklist = unblocklistfile.readlines()
    for username in unblocklist:
        #checkshutoff(taskname)
        user = p.User(title = username, site = site)
        print(user.isBlocked())
        ###user.unblock(reason = "Mass unblock of indefinitely blocked proxy blocks per [[WP:AN|this discussion]]")

import sys
import re
import time
import pywikibot as p

site = p.Site()
site.login()
if not site.logged_in(): print("Not logged in?"); sys.exit()

def main(queries):
    def fix(text, name, loc, shift):
        stext = text[loc[0]:loc[1]]
        hname = "<"+name+">"
        hcname = "</"+name+">"
        ef = 0
        if name in ("tt", "s", "u", "b", "i", "code", "strike"):
            search = re.findall(hname, stext)
            searchlen = len(search)
            i = stext.find(hname)+len(hname)
            j = stext.find(hname, i)
            test = stext[i:j]
            if searchlen==2:
                if not((hcname in test) or ("{{" in test) or ("}}" in test) or (test == "")):
                    if name == "tt" and test=="reviewer":
                        stext = stext.replace(hname, "{{mono|", 1)
                        stext = stext.replace(hname, "}}", 1)
                        shift+=1
                    elif name == "strike":
                        stext = stext.replace(hname, "<s>", 1)
                        stext = stext.replace(hname, "</s>", 1)
                        shift-=9
                    else:
                        stext = stext[:i]+stext[i:].replace(hname, hcname, 1)
                        shift+=1
                    ef+=1
        text = text[:loc[0]]+stext+text[loc[1]:]
        return text, shift, ef
    pageids = []
    for query in queries:
        title = query["title"]
        pageid = query["pageid"]
        name = query["params"]["name"]
        if name in ("font", "small", "big"):
            continue
        if pageid in pageids: continue
        else: pageids.append(pageid)
        errors = p.data.api.ListGenerator("linterrors", lntcategories = "multiple-unclosed-formatting-tags", lntlimit = 500, lntpageid = pageid, site = site)
        page = p.Page(site, title)
        text = page.text
        shift = 0
        newtext = text
        allerrorsfixed = True
        lintId = 0
        first = True
        for error in errors:
            loc = error["location"]
            if first == True:
                lintId = str(error["lintId"])
                print(lintId)
                first = False
            loc[0]-=1
            loc[0]+=shift #everytime a fix is applied, the location is off because a / is added or other changes occur, so add shift
            loc[1]+=shift
            name = error["params"]["name"]
            newtext, shift, ef = fix(newtext, name, loc, shift)
            if ef == 0:
                allerrorsfixed = False #ef = errorsfixed, if unable to fix a particular error, all errors haven't been fixed
                break
        if lintId !=0: ids.write("\n"+str(lintId))
        if allerrorsfixed:
            page.text = newtext
            try:
                if p.Page(site, "User:Galobot/shutoff").text != "":
                    print("Bot shutoffed")
                    while 1:
                        time.sleep(60)
                        print("Checking shutoff...")
                        if p.Page(site, "User:Galobot/shutoff").text == "":
                            print("No longer shutoffed")
                            break
                page.save(summary = "[[User:Galobot#Task_1|Task 1]]: Fix [[Special:LintErrors|lint errors]] ([[Special:LintErrors/multiple-unclosed-formatting-tags|multiple unclosed formatting tags]])", minor = True) #edit page
            except p.exceptions.PageSaveRelatedError:
                print("Error")
                with open("errorsfile.txt", "a+") as errorsfile:
                    errorsfile.write("\n"+str(lintId))

try:
    for x in range (int(sys.argv[2])):
        print("Starting new cycle")
        with open("idsfile.txt", "r") as ids:
            idlist = ids.readlines()
            lastid = int(idlist[-2])
            print(lastid)
        queries = p.data.api.ListGenerator("linterrors", lntcategories = "multiple-unclosed-formatting-tags", lntfrom = lastid, lntlimit = sys.argv[1], site = site)
        queries.set_maximum_items(sys.argv[1])
        with open("idsfile.txt", "a+") as ids:
                main(queries)
except KeyboardInterrupt:
    print("interrupted")

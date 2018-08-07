import sys
import re
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
                    #print(searchlen, stext, name, end = " ")
                    stext = stext[:i]+stext[i:].replace(hname, hcname, 1)
                    shift+=1
                    ef+=1
        text = text[:loc[0]]+stext+text[loc[1]:]
        return text, shift, ef
    pageids = []
    for query in queries:
        title = query["title"]
        pageid = query["pageid"]
        titlefilename = "linterrors/"+title.replace("/", "-s-")
        if pageid in pageids: print("skipped"); continue
        else: pageids.append(pageid)
        page = p.Page(site, title)
        text = page.text
        errors = p.data.api.ListGenerator("linterrors", lntcategories = "multiple-unclosed-formatting-tags", lntpageid = pageid, site = site)
        shift = 0
        newtext = text
        allerrorsfixed = True
        for error in errors:
            loc = error["location"]
            loc[0]+=shift #everytime a fix is applied, the location is off because a / is added, so add shift
            loc[1]+=shift
            name = error["params"]["name"]
            newtext, shift, ef = fix(newtext, name, loc, shift)
            if ef == 0:
                allerrorsfixed = False
        def savecall(page, outcome):
            if not outcome:
                raise(outcome)
            else:
                with open("linterrors/editsmade", "r") as editfile: editsmade = editfile.read()
                with open("linterrors/editsmade", "w") as editfile: editfile.write(str(int(editsmade)+1))
        if True:#allerrorsfixed:
            print(allerrorsfixed, title)
            #DO NOT UNCOMMENT page.save(newtext, summary = "[[User:Galobot#Task_1|Task 1]]: Fix [[Special:LintErrors|lint errors]] ([[Special:LintErrors/multiple-unclosed-formatting-tags|multiple unclosed formatting tags]])", minor = True) #edit page
            with open(titlefilename, "w") as textfile: textfile.write(newtext)
            #sys.exit()
            #site.throttle.wait(8)
queries = p.data.api.ListGenerator("linterrors", lntcategories = "multiple-unclosed-formatting-tags", lntfrom = 70366479, lntlimit = sys.argv[1], site = site)
queries.set_maximum_items(sys.argv[2])
main(queries)

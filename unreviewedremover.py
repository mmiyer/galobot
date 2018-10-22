from botbase import *
from operator import itemgetter
import mwparserfromhell

def logevent (action, title, review):#if review = 1, checking log of action of reviewing, if review = 0, checking log of action of unreviewing
    eventlist = []
    events = p.data.api.ListGenerator("logevents", leaction = action, letitle = title, site = site)
    for event in events:
        eventlist.append((event["timestamp"], review))
    return eventlist

numtemplates = sys.argv[1]
transclusions = p.data.api.ListGenerator("embeddedin", einamespace = "0", eilimit = numtemplates, eititle = "Template:New unreviewed article", site = site)
transclusions.set_maximum_items(numtemplates)

for transclusion in transclusions:
    title = transclusion["title"]
    pageactions = []
    #let's get all the relevant log actions of reviewing and unreviewing
    
        pageactions.extend(logevent("patrol/patrol", title, 1))
        pageactions.extend(logevent("pagetriage-curation/reviewed", title, 1))
        pageactions.extend(logevent("pagetriage-curation/unreviewed", title, 0))
    pageactions.sort(key = itemgetter(0))
    print(title, pageactions)
    if len(pageactions) > 0 and pageactions[-1][1] == 1:#latest action was a review, so let's remove the template
        page = p.Page(site, title)
        text = page.text
        wikicode = mwparserfromhell.parse(text)
        templates = wikicode.filter_templates()
        for templatename in ["New unreviewed article", "Unreviewed", "New", "NUA", "Nua", "Unreviewed article", "NUR"]:
            for template in templates:
                if template.name.matches(templatename):
                    wikicode.remove(template)
                    print (template, "removed from", title)
                    break #found the template, so no need to continue looping
        #page.text = str(wikicode)
        #########page.savewithshutoff(summary = "Remove [[Template:New unreviewed article]] from reviewed article")
        

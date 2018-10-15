import shelve
import datetime
import pywikibot as p

site = p.Site()
site.login()
if not site.logged_in(): print('Not logged in?'); sys.exit()

#current = {}
#categories = p.data.api.PageGenerator('categorymembers', gcmtitle = 'Category:Articles_with_missing_files', gcmnamespace = 0, site = site)
#categories.set_maximum_items(5)
#for page in categories:
    #title = page.title()
    #print(title)
    #images = next(iter(p.data.api.PropertyGenerator(prop = 'images', titles = title, site = site)))['images']
    #imagesjoined = '|'.join(image['title'] for image in images)
    #imageexist = p.data.api.Request(parameters = {'action' : 'query', 'titles' : imagesjoined, 'format' : 'json', 'formatversion' : '2'}, site = site).submit()
    #brokenimages = set()
    #for x in imageexist['query']['pages']:
        #if (not x.get('known')) and x.get('missing'):
            #brokenimages.add(x['title'])
    #current[title] = brokenimages

#with shelve.open('previous run.shelve') as previousrun:#figure out what new brokenfiles have been created since last run
    #new = {}
    #for key in current:
        #prevvalue = prev.get(key)
        #value = current.get(key)
        #if not prevvalue:
            #new[key] = value
        #else:#if title was in category yesterday, compare the lists and add if there's a new image
            #diff = value - prevvalue
            #if diff != set(): new[key] = diff
    #previousrun.prev.update(current)
with open('runlog', 'a+') as runlog:
    try:prevtime = runlog.readlines()[-1]
    except:prevtime = 
    runlog.write(str(datetime.datetime.utcnow().isoformat()))

new = {'Control (2007 film)': {'File:Control soundtrack cover.jpg'}, 'Country Club Bakery': {'File:Countryclub.jpg'}}
for title in new:
    images = new[title]
    revisions = p.data.api.PropertyGenerator(prop = 'revisions', rvstart = prevtime, rvprop = 'user|ids', titles = title, rvslots = 'main', site = site)
    for revision in revisions['query']['pages']:
        print(revision['revisions']['user'])
    #diffs = pywikibot.data.api.Request(parameters = {'action' : 'compare', 'fromid' : fromid, 'toid' : toid,  'format' : 'json', 'formatversion' : '2'}, site = site)

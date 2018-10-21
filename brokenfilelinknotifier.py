import shelve
import os
import datetime
from itertools import groupby
from galobotbase import *

categories = p.data.api.PageGenerator('categorymembers', gcmtitle = 'Category:Articles_with_missing_files', gcmnamespace = 0, site = site)
categories.set_maximum_items(100)
with shelve.open('current run.shelve') as current,  shelve.open('previous run.shelve') as prev:#open data of previous run to skip over titles already there
    for page in categories:
        title = page.title()
        if title in prev.keys() or title in current.keys():continue #if it was in previous run or this run got interrupted, skip
        print('Finding images of', title, '...')
        images = next(iter(p.data.api.PropertyGenerator(prop = 'images', titles = title, site = site)))['images']
        if len(images) > 500:continue #temporary skip
        imagesjoined = '|'.join(image['title'] for image in images)#TODO:Handle when >500 images - breaks "titles"  
        imageexist = p.data.api.Request(parameters = {'action' : 'query', 'titles' : imagesjoined, 'format' : 'json', 'formatversion' : '2'}, site = site).submit()
        brokenimages = set()
        for x in imageexist['query']['pages']:
            if (not x.get('known')) and x.get('missing'):#TODO:known seems to work well enough to know that it is a commons image but not documented. either find documentation or add an extra check to commmons?
                brokenimages.add(x['title'])
        print(title, 'has the broken images:', brokenimages)
        current[title] = brokenimages
    print('Comparing previous and current')
    current = prev #temporary for testing
    #prev = {}#temporary for testing
    new = {}
    for key in current:
        prevvalue = prev.get(key)
        value = current.get(key)
        if not prevvalue:
            new[key] = value
        else:#if title was in category yesterday, compare the lists and add if there's a new image
            diff = value - prevvalue
            if diff != set(): new[key] = diff
    print('Differences are:', new)

#os.rename('current run.shelve', 'previous run.shelve')
#os.remove('current run.shelve') #keep the same current and previous run for now

with open('runlog', 'r') as runlog:
    prevtime = runlog.readlines()[-1]
with open('runlog', 'a+') as runlog:
    pass
    #runlog.write('\n'+datetime.datetime.utcnow().isoformat())

users = {}
try:
    for title in new:
        images = new[title]
        print('Grabbing revisions of', title)
        #TODO:use pywikibot revisions functions
        revlist = p.data.api.PropertyGenerator(prop = 'revisions', rvstart = prevtime, rvprop = 'user|timestamp|ids', rvdir = 'newer', titles = title, site = site)
        revisions = []
        revdata = next(iter(revlist)).get('revisions')
        if not revdata:continue
        for slicedrev in revdata:
            revid = slicedrev['revid']
            parentid = slicedrev['parentid']
            timestamp = slicedrev['timestamp']
            user = slicedrev['user']
            revisions.append([user, parentid, revid])
        print('There are', len(revisions), 'reivisions')
        if len(revisions) > 20:
            continue #skip if there are too many revisions to not waste too many api calls
        imagepresences = {}
        for image in images: imagepresences[image] = []
        prevuser = ''
        prevrev = 0
        for revdata in revisions:
            print('Grabbing image data of', revdata)
            imagerevrequest = p.data.api.Request(parameters = {'action' : 'parse', 'oldid' : revdata[2], 'prop' : 'images', 'format' : 'json', 'formatversion' : '2'}, site = site).submit()
            imagerev = imagerevrequest['parse']['images']
            for image in images:
                imagepresences[image].append(1 if image[5:].replace(' ', '_') in imagerev else 0)
        for image in imagepresences:
            print('Processing presence of', image)
            presence = imagepresences[image]
            print(presence)
            reduced = [x[0] for x in groupby(presence)] #basically remove consecutive duplicates - reduce 0,0,0,0,1,1,1,1 to 0,1
            print(reduced)
            if reduced in([0,1], [1]): #check if broken image is only inserted once, if not ignore; needs to make sure when reduced = 1 that the first revision is actually that person adding the image - check the revision before; simple solution, grab one more revision in original call then can check if reduced == [0,1]
                badrevdata = revisions[presence.index(1)] #find where insertion occured, and then what revision it was done in and who did it
                user = badrevdata[0]
                diffdata = (badrevdata[1], badrevdata[2], title, image)
                if users.get(user):
                    users[user].append(diffdata)
                else:
                    users[user] = [diffdata]
except Exception as e:
    print(e)
    

for username in users:
    print('Checking the rights of', username, '...')
    #TODO:use pywikibot.page.User
    rights = next(iter(p.data.api.ListGenerator('users', ususers = username, usprop = 'rights', site = site))).get('rights')
    if rights and 'autoconfirmed' in rights:
        userdata = users[username]
        difflist = []
        for ud in userdata:
           difflist.append(''.join(('[[:', ud[3].replace('_', ' '), ']] to the page [[', ud[2].replace('_', ' '), ']] in this [[Special:Diff/', str(ud[0]), '/', str(ud[1]), '|diff]]')))
        multiple = (len (difflist) > 1)
        if multiple:
            difflist = [('\n* ' + x) for x in difflist]
        diffs = ''.join(difflist)
        print('Messaging', username, '...')
        print('Hello. Thank you for your recent edits. An automated process has found that you have added a link to ', 'the non-existent files:' if multiple else 'a non-existent file ', diffs,  '.' if not multiple else '\n', 'If you can, please remove or fix the file link. You may remove this message. To stop receiving these messages, see the opt-out instructions. ~~~~', sep = '')
#Remember to when adding saving functionality to add shutoff
#TODO:be more efficient when user makes multiple consecutive edits
#TODO:deal with first page creations with broken links nicely

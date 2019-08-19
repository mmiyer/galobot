'''
Parts from https://en.wikipedia.org/wiki/User:Ritchie333/afcbios.py, licensed CC-BY-SA-3.0
'''

import re
from botbase import *

titles = []
page_to_update = "Wikipedia:WikiProject Women in Red/Drafts"
reMarker = re.compile("<ref.*\/ref>|{{.*}}|<!--.*-->|\'\'\'|----")
reTitle = re.compile( '\(.*\)' )
header_new = "New Additions"
header_old = "Existing Pages"
wikitext = "{{/Header}}\n"
wikitext_header_2 = "== {} ==\n"
wikitext_header_3 = "=== {} - {} ===\n"
wikitext_entry = "* [[{}]]\n::<small><nowiki>{}</nowiki></small>\n:::<small><nowiki>{} - {}</nowiki></small>\n"
search_query = 'incategory:"AfC submissions declined as a non-notable biography" "{}"' 
keywords = [ "she was", "she is", "her book", "her work" ]

def run_search(keyword):
	page_query = p.data.api.ListGenerator(
		"search",
		srnamespace = 118,
		srsearch = search_query.format(keyword),
		srprop = "",
		site = site
	)
	return [page_result["title"] for page_result in page_query]

def generate_entries(titles, header):
	section_wikitext = wikitext_header_2.format(header)
	for num, title in enumerate(titles):
		if num % 50 == 0:
			section_wikitext += wikitext_header_3.format(num + 1, num + 50)
		page = p.Page(site, title)
		timestamp = str(page.latest_revision["timestamp"])[0:10]
		editsummary = page.latest_revision["comment"]
		shortText = reMarker.sub( '', page.text )
		shortTitle = reTitle.sub( '', title[6:] )
		sentences = re.search( shortTitle + '.*\.', shortText )
		if sentences is not None:
			firstsentence = sentences.group().partition( '.' )[0]
		else:
			firstsentence = ""
		section_wikitext += wikitext_entry.format(
			title, firstsentence, timestamp, editsummary
		)
	return section_wikitext

for keyword in keywords:
	titles += run_search(keyword)

titles = set(titles)

with open('last_titles.txt', 'r') as last_titles_file:
	last_titles = set(last_titles_file.read().split("|"))
with open('last_titles.txt', 'w') as last_titles_file:
	last_titles_file.write("|".join(titles))
	
new_titles = titles - last_titles
old_titles = titles & last_titles

wikitext += (generate_entries(new_titles, header_new) + generate_entries(old_titles, header_old))

page = p.Page(site, page_to_update)
page.text = wikitext
page.savewithshutoff(summary = 'Update "Women in Red drafts" report', minor = False)

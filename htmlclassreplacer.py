from botbase import *
import mwparserfromhell

htmlclass = "letterhead"
template_start = "{{letterhead start}}"
template_end = "{{letterhead end}}"
searchquery = ("insource:\"{0}\" insource:/class *= *[\"'][a-zA-Z0-9 ]*{0}/").format(htmlclass)
searchresults = p.data.api.ListGenerator("search", srsearch = searchquery, srnamespace = "*", srwhat = "text", srprop = "", site = site)
n = 50
searchresults.set_query_increment(n)
searchresults.set_maximum_items(n)

def node_filter(node):
	attrs = node.attributes
	if len(attrs) == 1:
		attr = attrs[0]
		if attr.name == "class" and attr.value.strip() == htmlclass:
			return True
	return False

for searchresult in searchresults:
	print(searchresult)
	title = searchresult["title"]
	page = p.Page(site, title)
	text = page.get()
	wikicode = mwparserfromhell.parse(text)
	nodes = wikicode.ifilter_tags(matches = node_filter)
	for node in nodes:
		end = "" if node.contents.endswith("\n") else "\n"
		new_markup = template_start + str(node.contents) + end +  template_end
		wikicode.replace(node, new_markup)
	#page.savewithshutoff(str(wikicode))

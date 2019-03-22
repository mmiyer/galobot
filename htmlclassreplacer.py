from botbase import *
import mwparserfromhell

tag = "div"
htmlclass = "letterhead"
template_start = "{{letterhead start}}"
template_end = "{{letterhead end}}"
searchquery = ("insource:\"{0}\" insource:/class *= *[\"'][a-zA-Z0-9 ]*{0}/").format(htmlclass)
searchresults = p.data.api.ListGenerator("search", srsearch = searchquery, srnamespace = "*", srwhat = "text", srprop = "", site = site)

def node_filter(node):
	attrs = node.attributes
	if len(attrs) == 1:
		attr = attrs[0]
		if node.tag == tag and attr.name == "class" and attr.value.strip() == htmlclass:
			return True
	return False

for searchresult in searchresults:
	title = searchresult["title"]
	page = p.Page(site, title)
	text = page.get()
	wikicode = mwparserfromhell.parse(text)
	nodes = wikicode.ifilter_tags(matches = node_filter)
	for node in nodes:
		end = "" if node.contents.endswith("\n") else "\n"
		new_markup = template_start + str(node.contents) + end +  template_end
		wikicode.replace(node, new_markup)
	new_text = str(wikicode)
	if page.text != new_text:
		page.text = new_text
		page.savewithshutoff(
			summary = 'Replacing uses of "{}" class with template ([[Wikipedia:Bots/Requests for approval/Galobot 3|BRFA]])'.format(htmlclass),
			minor = True,
			force=True
		)
	else:
		print('Could not save "{}"'.format(title))
		continue
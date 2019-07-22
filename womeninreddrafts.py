from botbase import *

titles = []
page_to_update = "Wikipedia:WikiProject Women in Red/Drafts"
wikitext = "{{{0}/Header}}".format(page_to_update)
wikitext_header_2 = "== {0} ==\n"
wikitext_header_3 = "== {0} - {1} ===\n"
wikitext_entry = "* [[{0}]]\n::<small>{1} - {2}</small>\n:::<small><nowiki>{4}</nowiki></small>\n"
search_query = 'incategory:"AfC submissions declined as a non-notable biography" "%s"' 
keywords = [ "she was", "she is", "her book", "her work" ]

def run_search(keyword):
	page_query = p.data.api.ListGenerator(
		"search",
		srnamespace = 118,
		srsearch = search_query.format(keyword),
		srprop = "",
		srlimit = 5,
		site = site
	)
	page_query.set_maximum_items(5)
	print([page_result["title"] for page_result in page_query])

def generate_entries(titles, header):
	section_wikitext = wikitext_header_2.format(header)
        for num, title in enumerate(titles):
		if num % 50 == 0:
			section_wikitext += wikitext_header_3.format(num + 1, num + 50)
                page = p.Page(title)
                timestamp = page.latest_revision["timestamp"]
                editsummary = page.latest_revision["comment"]
                firstsentence = next(iter(p.data.api.PropGenerator(
                        "extracts",
                        exsentences = 1,
                        titles = title,
                        site = site
                )))     
                page_data = [title, timestamp, editsummary, firstsentence]
                section_wikitext += wikitext_entry.format(page_data)

for keyword in keywords:
	titles += run_search(keyword)

titles = set(titles)

with open('last_titles.txt', 'r+') as last_titles_file:
	last_titles = set(last_titles_file.read_lines().split("|"))
	last_titles_file.seek(0)
	last_titles_file.write("|".join(titles))
	
new_titles = titles - last_titles
old_titles = titles & last_titles

wikitext = generate_entries
print(wikitext)

p.Page(site, page_to_update)

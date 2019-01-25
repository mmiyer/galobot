import regex
from botbase import *

args = sys.argv

query = p.data.api.ListGenerator("abuselog", aflprop = "details", aflfilter = args[1], site = site)
query.set_maximum_items(args[2])
query.set_query_increment(50)

extra = r".{0,20}"
pattern = regex.compile (r"(?V1)"+extra+r"(?:"+input("Regex: ")+r")"+extra, flags = regex.IGNORECASE)

for hit in query:
	details = hit["details"]
	new_wikitext = details["new_wikitext"]
	#added_lines = details.get("added_lines")
	if new_wikitext:
		match = pattern.search(new_wikitext)
		if match: print(match.group())

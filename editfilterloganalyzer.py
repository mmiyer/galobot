import regex
from botbase import *

args = sys.argv

query = p.data.api.ListGenerator("abuselog", aflprop = "details", aflfilter = args[1], site = site)
query.set_maximum_items(args[2])
query.set_query_increment(50)

extra = r".{,100}"
pattern = regex.compile (r"(?V1)"+extra+r"(?:"+input("Regex: ")+r")"+extra, flags = regex.IGNORECASE)

for hit in query:
	details = hit["details"]
	var = details.get(args[3])
	if var:
		match = pattern.search(var)
		if match: print(details["page_title"], match.group())

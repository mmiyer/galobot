from botbase import *
import re

valid_html = '<th style="background: #CCC;" class="headerSort" tabindex="0" role="columnheader button" title="Sort ascending">Area&nbsp;(km²)</th>'
#from turks and caicos islands

search = r'insource:"wikitable sortable" insource:/wikitable sortable[^}]*?!style[^}]*background[^}]*?\|-/' #search may be missing some instances..see about that
betsearch = r'insource:"sortable" insource:/sortable[^-]*?![^-]*?background/' #maybe?
text = 'fffffffffffffffffffffff {| class = "wikitable sortable" \n !background: red" \n |-'
color_names_list = ["black", "silver", "gray", "white", "maroon", "red", "purple", "fuchsia", "green", "lime", "olive", "yellow", "navy", "blue", "teal", "aqua", "orange", "aliceblue", "antiquewhite", "aquamarine", "azure", "beige", "bisque", "blanchedalmond", "blueviolet", "brown", "burlywood", "cadetblue", "chartreuse", "chocolate", "coral", "cornflowerblue", "cornsilk", "crimson", "cyan", "darkblue", "darkcyan", "darkgoldenrod", "darkgray", "darkgreen", "darkgrey", "darkkhaki", "darkmagenta", "darkolivegreen", "darkorange", "darkorchid", "darkred", "darksalmon", "darkseagreen", "darkslateblue", "darkslategray", "darkslategrey", "darkturquoise", "darkviolet", "deeppink", "deepskyblue", "dimgray", "dimgrey", "dodgerblue", "firebrick", "floralwhite", "forestgreen", "gainsboro", "ghostwhite", "gold", "goldenrod", "greenyellow", "grey", "honeydew", "hotpink", "indianred", "indigo", "ivory", "khaki", "lavender", "lavenderblush", "lawngreen", "lemonchiffon", "lightblue", "lightcoral", "lightcyan", "lightgoldenrodyellow", "lightgray", "lightgreen", "lightgrey", "lightpink", "lightsalmon", "lightseagreen", "lightskyblue", "lightslategray", "lightslategrey", "lightsteelblue", "lightyellow", "limegreen", "linen", "magenta", "mediumaquamarine", "mediumblue", "mediumorchid", "mediumpurple", "mediumseagreen", "mediumslateblue", "mediumspringgreen", "mediumturquoise", "mediumvioletred", "midnightblue", "mintcream", "mistyrose", "moccasin", "navajowhite", "oldlace", "olivedrab", "orangered", "orchid", "palegoldenrod", "palegreen", "paleturquoise", "palevioletred", "papayawhip", "peachpuff", "peru", "pink", "plum", "powderblue", "rosybrown", "royalblue", "saddlebrown", "salmon", "sandybrown", "seagreen", "seashell", "sienna", "skyblue", "slateblue", "slategray", "slategrey", "snow", "springgreen", "steelblue", "tan", "thistle", "tomato", "turquoise", "violet", "wheat", "whitesmoke", "yellowgreen", "rebeccapurple"]
color_names = "|".join(color_names_list)
extract_pattern = re.compile(r"sortable.*?\|-", re.DOTALL)
replace_pattern = re.compile(r"background:(\s*(?:#[\dA-F]+|{0})\s*[;\"'])".format(color_names), re.IGNORECASE)

for match in extract_pattern.finditer(text):
	old_match_text = match.group()
	new_match_text = replace_pattern.sub(r"background-color:\1", old_match_text)
	text = text[:match.start()] + new_match_text + text[match.end():]
print(text)
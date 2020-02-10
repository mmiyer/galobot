from botbase import *
import mwparserfromhell
import re

cs2_template_canonical_name = "Citation"
cs1_template_names = [
    "Cite arXiv",
    "Cite AV media",
    "Cite AV media notes",
    "Cite book",
    "Cite conference",
    "Cite encyclopedia",
    "Cite episode",
    "Cite interview",
    "Cite journal",
    "Cite magazine",
    "Cite mailing list",
    "Cite map",
    "Cite news",
    "Cite newsgroup",
    "Cite podcast",
    "Cite press release",
    "Cite report",
    "Cite serial",
    "Cite sign",
    "Cite speech",
    "Cite techreport",
    "Cite thesis",
    "Cite web",
]
cs2_template_names = [
    "Citation",
    "Cite",
    "Cite study",
    "Cite technical standard",
    "Cite Technical standard",
    "Cite citation",
    "Ouvrage",
    "Bokref",
]
replacement_map = {"Cite book": ["ISBN", "Isbn"]}
transclusions = p.data.api.ListGenerator(
    "embeddedin",
    eititle="Template:" + cs2_template_canonical_name,
    einamespace=0,
    site=site,
)
transclusions.set_maximum_items(5)


def change_template(node, new_name):
    print(node)
    pattern = re.compile(
        r"^(?P<pre>{{{{\s*)({0})(?P<aft>\s*\|)".format(str(node.name)), re.IGNORECASE
    )
    return pattern.sub(r"\g<pre>" + new_name + r"\g<aft>", str(node))


for transclusion in transclusions:
    title = transclusion["title"]
    print("\n" + title)
    page = p.Page(site, title)
    text = page.get()
    wikicode = mwparserfromhell.parse(text)
    cs1_templates = wikicode.filter_templates(
        matches=lambda template: template.name.matches(cs1_template_names)
        and not template.has("mode")
    )
    cs2_templates = wikicode.filter_templates(
        matches=lambda template: template.name.matches(cs2_template_names)
        and not template.has("mode")
    )
    if 1 <= len(cs2_templates) <= 3 and len(cs1_templates) / len(cs2_templates) >= 5:
        for cs2_template in cs2_templates:
            print(cs2_template)
            # cs2_template.has(param, ignore_empty=True)
            # new_template = change_template(cs2_template, "Cite book")
            # print(new_template)
            # wikicode.replace(cs2_template, new_template)

from botbase import *
import difflib

prompt1 = '''
The following is a diff of an edit made on Wikipedia, to the article on "{}".
The last line of your response must be the the probability that this edit is vandalism, using the Wikipedia definition of vandalism, and must fit this format string: "0.%d%d%d" exactly.
'''

prompt2 = '''
You're an AI designed to detect vandalism on Wikipedia. The following is a diff of an edit made on Wikipedia, to the article on "{}".
First explain if the edit is vandalism and then determine yes or no if the edit is vandalism that should be reverted.
The last line of your response must be the probability that this edit is vandalism,using the Wikipedia definition of vandalism, and must fit this format string: "0.%d%d%d" exactly.
'''

prompt3 = '''
You're an AI designed to classify edits on Wikipedia into "vandalism", "spam", "disruptive", or "good-faith". The following is a diff of an edit made on Wikipedia, to the article on "Atique Ahmed". Determine which of the categories the edit falls into and if it should be reverted.
The last line of your response must be the the probability that this edit is vandalism, using the Wikipedia definition of vandalism, and must fit this format string: "0.%d%d%d" exactly.
'''

recentchanges = site.recentchanges(
    namespaces = "0",
    changetype = "edit",
    bot = False,
    total = 1000
)
newuser_recentchanges = filter(
    lambda edit: not "confirmed" in "".join(p.page.User(site, title = edit["user"]).groups()),
    recentchanges
)
for edit in newuser_recentchanges:
    page = p.page.Page(site, edit["title"])
    new_revision_text = page.getOldVersion(edit["revid"]).splitlines(keepends=True)
    old_revision_text = page.getOldVersion(edit["old_revid"]).splitlines(keepends=True)
    diff = "".join(difflib.unified_diff(old_revision_text, new_revision_text))
    full_prompt = prompt2.format(edit['title']) + "\n" + diff
    with open(f"diffs/{str.replace(edit['title'], '/', '')}", "w") as f:
        f.write(full_prompt)

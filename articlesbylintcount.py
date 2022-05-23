import toolforge
import pymysql
from botbase import *

conn = toolforge.connect('enwiki', cluster = "analytics" )
query = '''
select page_title, count(*) as page_count
from linter
join page on page.page_id = linter.linter_page
where page.page_namespace=0 and linter_cat != 2
group by page.page_id
order by count(*) desc, page_title asc
limit 1000;
'''

tablerows = []
with conn.cursor(pymysql.cursors.DictCursor) as cur:
    cur.execute(query)
    data = cur.fetchall()
    for row in data:
        page_title = row.pop('page_title').decode()
        tablerows.append('\n|-\n|[[' + page_title.replace('_', ' ') + ']]')
        tablerows.append('\n|' + '[https://en.wikipedia.org/wiki/Special:LintErrors?pagename=' + page_title + ' lints]')
        for param in ['page_count']:
            tablerows.append('\n|' + str(row[param] or ''))
    
    page = p.Page(site, 'User:Galobot/report/Articles_by_Lint_Errors')
    page.text = ('Generated by [[Quarry:query/31876|this query]].' +
                ' Excludes [[Special:LintErrors/obsolete-tag|obsolete HTML tag lint errors]].' +
                ' Updated on ~~~~~. ' +
                '\n{| class="wikitable sortable"\n!Page title\n!Lint list\n!Lint errors' +
                ''.join(tablerows) +
                '\n|}')
    page.savewithshutoff(summary = 'Update "Articles by Lint Errors" report', minor = False) #edit page

conn.close()

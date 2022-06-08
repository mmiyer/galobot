from botbase import *
import mwparserfromhell

SIZE_MAPPING = {
    1: 'x-small',
    2: 'small',
    3: 'medium',
    4: 'large',
    5: 'x-large',
    6: 'xx-large',
    7: 'xxx-large'
}
    
def main(queries):
    for query in queries:
        title = query['title']
        page = p.Page(site, title)
        text = page.get()
        wikicode = mwparserfromhell.parse(text)
        font_tags = wikicode.ifilter_tags(matches = lambda node: node.tag == "font")
        for tag in font_tags:
            tag.tag = 'span'
            color, face, size = '', '', ''
            if tag.has('color'):
                rawcolor = str(tag.get('color').value)
                tag.remove('color')
                # https://stackoverflow.com/questions/11592261/check-if-a-string-is-hexadecimal
                try:
                    int(rawcolor, 16)
                    pcolor = f'#{rawcolor}'
                except ValueError:
                    pcolor = rawcolor
                color = f'color: {pcolor};'

            if tag.has('face'):
                rawface = str(tag.get('face').value)
                face = f'font-family: {rawface};'
                tag.remove('face')

            if tag.has('size'):
                rawsize = str(tag.get('size').value)
                size = f'font-size: {SIZE_MAPPING[rawsize]};'
                tag.remove('size')

            if color or face or size:
                #FIXME: if contents wrapped by an inner tag, migrate style to that tag
                if tag.has('style'):
                    styleattr = tag.get('style')
                else:
                    styleattr = tag.add('style')
                
                if not styleattr.value:
                    styleattr.value = ''
                
                styleattr.value.append(' '.join(filter(None, [color, face, size])))

                if color:
                    #TODO: match Tidy's behaviour
                    for wikilink in tag.contents.ifilter_wikilinks():
                        otext = wikilink.text
                        #FIXME: also migrate style to inner tag, might already be set so don't set twice
                        linktag = mwparserfromhell.nodes.tag.Tag('span', contents = otext)
                        linktag.add('style', value = color)
                        wikilink.text = linktag
        new_text = str(wikicode)
        if page.text != new_text:
            page.text = new_text
            page.savewithshutoff(
                summary = 'Fix lint errors (test)', #([[Wikipedia:Bots/Requests for approval/Galobot 5|BRFA]])'
                shutoff = "linterrorfixer",
                minor = True,
                force = True,
            )
        else:
            print('Could not save "{}"'.format(title))
            continue

try:
    # for x in range(int(sys.argv[2])):
    #     print("Starting new cycle")
    #     with open("idsfile.txt", "r") as ids:
    #         idlist = ids.readlines()
    #         lastid = int(idlist[-2])
    #         print(lastid)
        #queries = p.data.api.ListGenerator("linterrors", lntnamespace = "*", lntcategories = "obsolete-tag", lntlimit = sys.argv[1], site = site)
        #queries.set_maximum_items(sys.argv[1])
    queries =[{'title': 'User:Galobot/sandbox'}]
    with open("idsfile.txt", "a+") as ids:
        main(queries)
except KeyboardInterrupt:
    print("interrupted")

import re
import os

def writetofile(out_filename, text):
    with open(os.path.expanduser(out_filename), 'w+') as out_file:
        out_file.write(str(text))

def replaceahref(dom, pattern, replace):
    a_links = dom.xpath("//a[@href]")
    for link in a_links:
        id = re.search(pattern, link.attrib['href'])
        if id is not None:
            if 'target' in link.attrib:
                link.attrib.pop('target')
            link.attrib['href'] = replace(id)
    return dom

def rmelement(dom, xpath):
    elements = dom.xpath(xpath)
    for element in elements:
        element.getparent().remove(element)
    return dom

def updelement(dom, tag, attri, repl):
    elements = dom.xpath('//%s[@%s]' % (tag, attri))
    for element in elements:
        element.attrib[attri] = repl(element.attrib[attri])
    return dom

def rmattrib(dom, tag, attrib):
    elements = dom.xpath('//%s[@%s]' % (tag, attrib))
    for element in elements:
        element.attrib.pop(attrib)
    return dom
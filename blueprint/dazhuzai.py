from flask import Blueprint
import requests
from lxml import html
from lxml.html import builder as E
import re
import logging


dazhuzai_bp = Blueprint('dazhuzai', __name__)

target_base_url = 'https://www.luoxia.com/dazhuzai/'
cookies = {}

@dazhuzai_bp.route('/')
def index():
    r = requests.get(target_base_url)
    cookies.update(r.cookies.items())
    dom = cleanads(html.fromstring(r.text))
    return html.tostring(pagify(dom), pretty_print=True)

@dazhuzai_bp.route('/page/<id>')
def page(id):
    headers = {}
    headers['User-Agent'] = 'PostmanRuntime/7.17.1'
    headers['Host'] = 'www.luoxia.com'
    headers['Cache-Control'] = 'no-cache'
    url = target_base_url + id + '.htm'
    print(cookies)
    r = requests.get(url, headers=headers, cookies=cookies)
    print(r.status_code)
    print(r.request.headers)
    dom = cleanads(html.fromstring(r.text))
    return html.tostring(pagify(dom), pretty_print=True)

def pagify(dom):
    search_pattern = target_base_url + r'(?P<id>\d+).htm'
    a_links = dom.xpath("//a[@href]")
    for link in a_links:
        id = re.search(search_pattern, link.attrib['href'])
        if id is not None:
            if 'target' in link.attrib:
                link.attrib.pop('target')
            link.attrib['href'] = '/page/' + str(id.group('id'))

    b_links = dom.xpath("//b[@onclick]")
    for link in b_links:
        id = re.search(search_pattern, link.attrib['onclick'])
        if id is not None:
            new_href = '/page/' + str(id.group('id'))
            new_tag = E.A(link.text_content(), title=link.attrib["title"], href=new_href)
            parent_node = link.getparent()
            parent_node.replace(link, new_tag)

    p_tags = dom.xpath("//div[@id='nr1']/p")
    for p in p_tags:
        if (('class' in p.attrib and p.attrib['class'] == 'pcinvisible') 
                or (re.search('落.*霞.*小.*说', p.text_content()) is not None)):
            # print(p.text_content())
            p.getparent().remove(p)
    return dom

def cleanads(dom):
    async_scripts = dom.xpath("//script[@async]")
    for script_tag in async_scripts:
        script_tag.getparent().remove(script_tag)
    return dom
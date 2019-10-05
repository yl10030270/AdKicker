from flask import Blueprint
import requests
from lxml import html
import os

import re

zhongjidouluo_bp = Blueprint('zhongjidouluo', __name__)

target_base_url = 'http://www.jueshitangmen.info/zhongjidouluo/'
cookies = {}

@zhongjidouluo_bp.route('/')
def index():
    r = requests.get(target_base_url)
    dom = html.fromstring(r.text);
    rmelm(dom, "//script")
    return html.tostring(pagify(dom, target_base_url), pretty_print=True)


@zhongjidouluo_bp.route('/page/<id>')
def page(id):
    url = target_base_url + id + '.html'
    r = requests.get(url)
    dom = html.fromstring(r.text)
    rmelm(dom, "//center")
    rmelm(dom, "//script")
    home_links = dom.xpath("//a[@href='" + target_base_url + "']")
    for hl in home_links:
        hl.attrib['href'] = '/'
    return html.tostring(pagify(dom, target_base_url), pretty_print=True)

def writetofile(out_filename, text):
    with open(os.path.expanduser(out_filename), 'w+') as out_file:
        out_file.write(str(text))

def pagify(dom, base_url):
    search_pattern = base_url + '(?P<id>\d+).htm';
    a_links = dom.xpath("//a[@href]")
    for link in a_links:
        id = re.search(search_pattern, link.attrib['href'])
        if id is not None:
            if 'target' in link.attrib:
                link.attrib.pop('target')
            link.attrib['href'] = '/page/' + str(id.group('id'))
    return dom

def rmelm(dom, xpath):
    elements = dom.xpath(xpath)
    for element in elements:
        element.getparent().remove(element)
    return dom

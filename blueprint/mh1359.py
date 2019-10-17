from flask import Blueprint, url_for, redirect, request
import requests
from lxml import html
from .util import replaceahref, rmelement, updelement
from urllib.parse import urljoin 
import re

PRE_FIX = 'mh139'
BASE_URL = 'https://m.mh1359.com/'

mh1359_bp = Blueprint(PRE_FIX, __name__)
myparser = html.HTMLParser(encoding="UTF-8")

@mh1359_bp.route('/')
def index():
    r = requests.get(BASE_URL)
    dom = html.fromstring(r.text, parser=myparser)
    dom = transform(dom)
    return html.tostring(dom, pretty_print=True)

@mh1359_bp.route('/manhua/<idpage>')
def manhua(idpage):
    r = requests.get(urljoin(BASE_URL, 'manhua/' + idpage))
    dom = html.fromstring(r.text, parser=myparser)
    dom = transform(dom)
    return html.tostring(dom, pretty_print=True)

@mh1359_bp.route('/chapter/<idpage>')
def chapter(idpage):
    r = requests.get(urljoin(BASE_URL, 'chapter/' + idpage))
    dom = html.fromstring(r.text, parser=myparser)
    dom = transform(dom)
    dom = rmelement(dom, "//div[@class='bt-banner']")
    return html.tostring(dom, include_meta_content_type=True, encoding='UTF-8', pretty_print=True)

def transform(dom):
    dom = updelement(dom, 'link', 'href', lambda s: urljoin(BASE_URL, s))
    dom = updelement(dom, 'img', 'src', lambda s: urljoin(BASE_URL, s))
    dom = updelement(dom, 'script', 'src', lambda s: urljoin(BASE_URL, s) if s.startswith('/') else s )
    dom = replaceahref(dom, r'/manhua/(?P<id>\d+)', lambda id : url_for('.manhua', idpage=id.group('id')))
    dom = replaceahref(dom, r'/chapter/(?P<id>\d+.html)', lambda id : url_for('.chapter', idpage=id.group('id')))
    return dom

def is_mh139url(url):
    return (re.search(r'/js/\d+.undefined.js', url) is not None or 
            re.search(r'/api/updateview/', url) is not None)
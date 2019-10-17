from flask import Blueprint, url_for
import requests
from lxml import html
from .util import replaceahref, rmelement, updelement, rmattrib

import re

PRE_FIX = 'zhongjidouluo'
BASE_URL = 'http://www.jueshitangmen.info/zhongjidouluo/'

zhongjidouluo_bp = Blueprint(PRE_FIX, __name__)


@zhongjidouluo_bp.route('/')
def index():
    r = requests.get(BASE_URL)
    dom = html.fromstring(r.text)
    rmelement(dom, "//script")
    replaceahref(dom, BASE_URL + r'(?P<id>\d+).htm', lambda id : url_for('.page', id=id.group('id')))
    return html.tostring(dom, pretty_print=True)


@zhongjidouluo_bp.route('/page/<id>')
def page(id):
    url = BASE_URL + id + '.html'
    r = requests.get(url)
    dom = html.fromstring(r.text)
    rmelement(dom, "//center")
    rmelement(dom, "//script")
    updelement(dom, 'a', 'href', lambda h : url_for('.index') if h == BASE_URL else h)
    rmattrib(dom, 'a', 'target')
    replaceahref(dom, BASE_URL + r'(?P<id>\d+).htm', lambda id : url_for('.page', id=id.group('id')))
    return html.tostring(dom, pretty_print=True)




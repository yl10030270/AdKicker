import requests
from lxml import html

from flask import Flask
app = Flask(__name__)

@app.route('/')
def index():
    r = requests.get('https://www.luoxia.com/dazhuzai/')
    dom = html.fromstring(r.text)
    links = dom.xpath("//a[@href]")
    for link in links:
        link.attrib['href'] = '/page'
    return html.tostring(dom, pretty_print=True)

@app.route('/page')
def page():    
    return 'hello, world!'
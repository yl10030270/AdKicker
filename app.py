from flask import Flask, redirect, request, abort
from blueprint import zhongjidouluo_bp, mh1359_bp, is_mh139url, MH139_BASE_URL
from urllib.parse import urljoin 

app = Flask(__name__)
app.register_blueprint(mh1359_bp, url_prefix='/' + mh1359_bp.name)
app.register_blueprint(zhongjidouluo_bp, url_prefix='/' + zhongjidouluo_bp.name)

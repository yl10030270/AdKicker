from flask import Flask
from zhongjidouluo import zhongjidouluo_bp

app = Flask(__name__)
app.register_blueprint(zhongjidouluo_bp)

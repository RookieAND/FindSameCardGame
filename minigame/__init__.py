from flask import Flask

from minigame.config.default import config_by_name
from minigame.utils.account import account
from minigame.utils.register import signup
from minigame.user_page import main
from minigame.utils.email import mail


def create_app(config_name='dev'):
    app = Flask(__name__)
    app.config.from_object(config_by_name[config_name])

    # 블루프린트 핸들링 파트
    app.register_blueprint(account)
    app.register_blueprint(main)
    app.register_blueprint(signup)

    mail.init_app(app)

    return app

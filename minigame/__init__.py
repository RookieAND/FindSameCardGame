from flask import Flask, render_template, session
from minigame.user_account import account
from minigame.user_page import main

app = Flask(__name__)
app.secret_key = "minigameweb"

# 블루프린트 핸들링 파트 (account, etc)
app.register_blueprint(account)
app.register_blueprint(main)
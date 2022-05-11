from random import randint

import bcrypt

from minigame.utils.form import RegisterForm, LoginForm, RegConfirmForm
from minigame.utils.database import account_register, account_exist
from minigame.utils.email import send_validate_email

from flask import Blueprint, session, url_for, redirect, request, render_template, flash, jsonify

signup = Blueprint('signup', __name__, url_prefix='/')


@signup.route('/register', methods=['GET', 'POST'])
def register():
    # 이미 로그인이 된 상태라면, 다시 메인 페이지로 돌려 보냄.
    if 'loggedIn' in session:
        return redirect(url_for('main.main_page'))

    # 맨 처음 접속할 경우 GET 메소드로 요청이 오므로, 로그인 템플릿 제공
    form = RegisterForm(request.form)

    return render_template("register.html", form=form)


@signup.route('/register/validation', methods=['POST'])
def register_check_vaild():
    # 회원 가입 전용 FlaskForm 객체인 RegisterForm 생성
    form = RegisterForm(request.form)
    # 먼저, form 에 아이디와 비밀번호가 전부 적혔는지를 먼저 체크함.
    if form.validate():
        form_info = {
            'username': form.username.data,
            'password': form.password.data,
            'email': form.email.data
        }

        if account_exist(form_info['username'])['is_exists']:
            return jsonify(result='fail', status=200, reason='해당 ID는 이미 다른 유저가 사용 중입니다.')
        else:
            confirm_password = randint(100000, 999999)
            send_validate_email(form_info['email'], confirm_password)
            return jsonify(result='success', status=200, confirm_pw=confirm_password)

    return jsonify(result='fail', status=200, reason='회원가입에 필요한 정보를 모두 올바르게 작성해주세요.')


@signup.route('/register/confirm', methods=['POST'])
def confirm_verify_email():

    regForm = RegConfirmForm(request.form)


    flash("해당 인증 이메일은 이미 만료되었거나 유효하지 않습니다.")
    # 입력 받은 비밀번호를 String -> Bytes 타입으로 변경 후 Bcrypt 를 사용하여 암호화 진행.
    # 그 후 암호화 된 데이터를 String으로 복호화 하여 DB에 해당 내용을 저장시킴. (그대로 저장 시 문제 발생)
    password = (bcrypt.hashpw(password.encode('UTF-8'), bcrypt.gensalt())).decode('utf-8')
    account_register(username, password, email)
    login_form = LoginForm()
    flash("가입이 완료되었습니다. 생성된 계정으로 로그인하세요.")
    return render_template("login.html", form=login_form)
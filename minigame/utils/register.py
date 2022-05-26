from random import randint

import bcrypt

from minigame.utils.form import RegisterForm, LoginForm
from minigame.utils.database import account_register, account_exist, account_confirm, account_is_confirmed
from minigame.utils.email import confirm_token, generate_confirmation_token, send_validate_email

from flask import Blueprint, session, url_for, redirect, request, render_template, flash, jsonify

signup = Blueprint('signup', __name__, url_prefix='/')


@signup.route('/register')
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
        # form에서 받아온 ID, PW, Email 정보를 저장함.
        username = form.username.data
        password = form.password.data
        email = form.email.data

        # 먼저, 해당 계정이 이미 인증되었는지를 체크해야 함.
        if account_is_confirmed(email):
            return jsonify(result='fail', errcode='002', status=200)
        else:
            # 만약 계정을 처음 생성하려고 시도했다면, DB에 새롭게 정보를 적재시킴.
            # 인증 URL이 만료된 케이스의 경우 정보를 적재하지 않고 인증 메일 전송.
            if not account_exist(username):
                password = (bcrypt.hashpw(password.encode('UTF-8'), bcrypt.gensalt())).decode('utf-8')
                account_register(username, password, email)

            # email을 포함하여 새로운 랜덤 난수 토큰을 생성하고, 이를 url에 할당시킴.
            token = generate_confirmation_token(email)
            confirm_url = url_for('signup.confirm_verify_email', token=token, _external=True)
            html = render_template('email.html', confirm_url=confirm_url)
            subject = "FindSamePicture 미니게임 계정 인증"

            # 제목, html 템플릿, url을 전달하여 사용자에게 인증 메일을 전송함.
            send_validate_email(email, subject, html)
            return jsonify(result='success', status=200)

    return jsonify(result='fail', errcode='001', status=200)


@signup.route('/register/<token>')
def confirm_verify_email(token):

    email = confirm_token(token)
    # 이메일 기간 만료 시 False 리턴, 이를 체크하여 회원 가입 페이지로 보냄.
    if not email:
        flash('URL 인증 기간이 만료되었습니다. 처음부터 진행해주세요.')
        return redirect(url_for('signup.register'))

    if account_is_confirmed(email):
        flash('이미 인증이 완료된 계정입니다. 로그인을 해주세요.')
        return redirect(url_for('account.login'))
    else:
        account_confirm(email)
        flash("가입이 완료되었습니다. 생성된 계정으로 로그인하세요.")
        return redirect(url_for('account.login'))

    return redirect(url_for('main.mypage'))

from minigame.utils.form import LoginForm
from minigame.utils.database import account_login

from datetime import timedelta
from flask import Blueprint, flash
from flask import redirect, render_template, session, request, url_for

account = Blueprint('account', __name__, url_prefix='/')


# 세션 만료 기간을 5분으로 설정하기 위한 섹션.
@account.before_request
def setting_session_live():
    session.permanent = True
    account.permanent_session_lifetime = timedelta(minutes=5)


@account.route('/login', methods=['POST', 'GET'])
def login():
    # 이미 로그인이 된 상태라면, 다시 메인 페이지로 돌려 보냄.
    if 'loggedIn' in session:
        return redirect(url_for('main.main_page'))

    # 로그인 전용 FlaskForm 객체인 LoginForm 생성
    form = LoginForm(request.form)

    if request.method == 'POST':
        # form 에 아이디와 비밀번호가 전부 적혔는지를 먼저 체크함.
        if form.validate():
            username = form.username.data
            password = form.password.data

            # 해당 ID와 PW를 가진 계정이 있는지, PW가 올바른지를 체크해야 함.
            if not account_login(username, password):
                flash("입력하신 정보의 계정은 존재하지 않습니다.")
                return render_template("login.html", form=form)

            session['loggedIn'] = True
            session['username'] = username
            return redirect(url_for('main.main_page'))

        # 아이디와 비밀번호가 올바르게 적히지 않았다면, 리다이렉트 진행
        else:
            flash("올바른 ID와 PW를 입력해주세요.")
            return render_template("login.html", form=form)

    # 맨 처음 접속할 경우 GET 메소드로 요청이 오므로, 로그인 템플릿 제공
    flash('로그인을 하시려면 ID와 PW를 입력해주세요')
    return render_template("login.html", form=form)


@account.route('/logout')
def logout():
    # 로그아웃 진행 시 유저의 이름, 로그인 상태가 담긴 세션을 제거함
    session.pop('loggedIn', None)
    session.pop('username', None)
    return redirect(url_for('main.main_page'))

import re
import bcrypt
from datetime import timedelta
from flask import Blueprint
from flask import redirect, render_template, session, request, url_for

from minigame.user_data import account_login, account_exist, account_register

account = Blueprint('account', __name__, url_prefix='/')


# 세션 만료 기간을 5분으로 설정하기 위한 섹션.
@account.before_request
def setting_session_live():
    session.permanent = True
    account.permanent_session_lifetime = timedelta(minutes=5)


@account.route('/register', methods=['POST', 'GET'])
def register():
    # 이미 로그인이 된 상태라면, 다시 메인 페이지로 돌려 보냄.
    if 'loggedIn' in session:
        return redirect(url_for('main.main_page'))

    # 회원가입을 시도했다면, 이를 체크하여 조건 탐색을 시작함
    msg = '회원가입을 하시려면 ID와 PW를 입력해주세요.'
    if request.method == 'POST':
        # form 에 아이디와 비밀번호가 전부 적혔는지를 먼저 체크함.
        if 'username' in request.form and 'password' in request.form:
            username = request.form['username']
            password = request.form['password']
            email = request.form['email']

            # 유저가 정상적으로 회원가입이 가능한지를 판별해주는 함수를 실행
            problem = check_wrong_info(username, password, email)
            if problem is not None:
                return render_template("register.html", msg=problem)

            session['loggedIn'] = True
            session['username'] = username

            # 입력 받은 비밀번호를 String -> Bytes 타입으로 변경 후 Bcrypt 를 사용하여 암호화 진행.
            # 그 후 암호화 된 데이터를 String으로 복호화 하여 DB에 해당 내용을 저장시킴. (그대로 저장 시 문제 발생)
            password = (bcrypt.hashpw(password.encode('UTF-8'), bcrypt.gensalt())).decode('utf-8')
            account_register(username, password, email)
            msg = "가입이 완료되었습니다. 생성된 계정으로 로그인하세요."
            return render_template("login.html", msg=msg)

    # 맨 처음 접속할 경우 GET 메소드로 요청이 오므로, 로그인 템플릿 제공
    return render_template("register.html", msg=msg)


def check_wrong_info(username, password, email):
    # ID / 비밀번호 양식이 올바른지를 먼저 체크해야 함. (id, pw를 합쳐 한번에 판별)
    if re.match('[a-zA-Z0-9]', username + password) is None:
        msg = "ID와 비밀번호는 영문과 숫자로만 기입하세요."
        return msg

    # ID / 비밀번호 길이가 20자를 넘기지 않는지를 체크해야 함.
    if len(username) > 20 or len(password) > 20:
        msg = "ID와 비밀번호는 최대 20글자까지 가능합니다."
        return msg

    # 이메일 양식이 올바른지를 먼저 체크해야 함. (email만 별도로 체크하여 판별)
    email_regex = "^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$"
    if re.match(email_regex, email) is None:
        msg = "올바른 이메일 양식을 입력하지 않았습니다."
        return msg

    # 해당 ID로 생성한 계정이 이미 있는지를 판별해야 함.
    is_exist = account_exist(username)['is_exists']
    print(is_exist)
    if is_exist:
        msg = "해당 ID는 이미 다른 유저가 사용 중입니다."
        return msg

    # 기준이 모두 충족되었다면, 아무런 문제가 없음을 알리는 None을 리턴시킴.
    return None


@account.route('/login', methods=['POST', 'GET'])
def login():
    # 로그인을 시도하였다면, 이를 세션에 저장하고 메인 페이지로 돌려줌.
    msg = '로그인을 하시려면 ID와 PW를 입력해주세요'

    if request.method == 'POST':
        # form 에 아이디와 비밀번호가 전부 적혔는지를 먼저 체크함.
        if 'username' in request.form and 'password' in request.form:
            username = request.form['username']
            password = request.form['password']

            # ID / 비밀번호 양식이 올바른지를 먼저 체크해야 함. (정규식으로 체크)
            if re.match('[a-zA-Z0-9]', username + password) is None:
                msg = "ID와 비밀번호는 영문과 숫자로만 기입하세요."
                return render_template("login.html", msg=msg)

            # 해당 ID와 PW를 가진 계정이 있는지를 DB에서 체크함. (pw는 암호화 진행)
            result = account_login(username, password)

            if result:
                session['loggedIn'] = True
                session['username'] = username
                return redirect(url_for('main.main_page'))

            else:
                msg = "올바르지 않은 ID 혹은 PW를 입력하셨습니다."
                return render_template("login.html", msg=msg)

        # 아이디와 비밀번호가 올바르게 적히지 않았다면, 리다이렉트 진행
        else:
            msg = "ID / PW를 입력하셔야 로그인이 가능합니다."
            return render_template("login.html", msg=msg)

    # 맨 처음 접속할 경우 GET 메소드로 요청이 오므로, 로그인 템플릿 제공
    return render_template("login.html", msg=msg)


@account.route('/logout')
def logout():
    # 로그아웃 진행 시 유저의 이름, 로그인 상태가 담긴 세션을 제거함
    session.pop('loggedIn', None)
    session.pop('username', None)
    return redirect(url_for('main.main_page'))

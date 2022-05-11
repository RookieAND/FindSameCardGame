from flask import current_app
from flask_mail import Message, Mail
from itsdangerous import URLSafeTimedSerializer

mail = Mail()


# 인증 URL에 사용되는 랜덤 TOKEN 값을 생성시키는 함수.
def generate_confirmation_token(email):
    serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    return serializer.dumps(email, salt=current_app.config['SECURITY_PASSWORD_SALT'])


# 인증 URL에서 유효한 Email 값을 추출하고, 이를 반환하는 함수 (유효 기간 10분)
def confirm_token(token, expiration=600):
    serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    try:
        email = serializer.loads(
            token,
            salt=current_app.config['SECURITY_PASSWORD_SALT'],
            max_age=expiration
        )
    # 만약 인증 시간이 다 되었다면, False를 리턴함.
    except:
        return False
    return email


def send_validate_email(player_email: str, subject: str, template: str):
    mail_msg = Message(subject, html=template,
                       sender=current_app.config['MAIL_USERNAME'], recipients=[player_email])
    mail.send(mail_msg)

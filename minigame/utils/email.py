from flask import current_app
from flask_mail import Message, Mail

mail = Mail()


def send_validate_email(player_email: str, confirm_pw: int):
    mail_msg = Message("Minigame Verify Email",
                       sender=current_app.config['MAIL_USERNAME'], recipients=[player_email])
    mail_msg.body = f"이메일 인증 번호 : {confirm_pw}"
    mail.send(mail_msg)
    return 'Send'

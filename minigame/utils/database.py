import bcrypt
import datetime
import pymysql
from pymysql import cursors
from pymysql.constants import CLIENT
from flask import current_app


def connect_mysql() -> tuple:
    # 수업 정보를 가져올 때마다 MySQL에 연결을 실행해야 함.
    user_db = pymysql.connect(
        host=current_app.config['MYSQL_HOST'],
        user=current_app.config['MYSQL_USER'],
        password=current_app.config['MYSQL_PASSWORD'],
        db=current_app.config['MYSQL_DB'],
        charset='utf8',
        client_flag=CLIENT.MULTI_STATEMENTS
    )
    # MySQL 의 Data 를 Dict 형태로 반환 시키는 DictCursor 사용
    cursor = user_db.cursor(cursors.DictCursor)
    return user_db, cursor


# 여기서부터는 계정과 관련된 함수들을 작성하는 파트 (계정이 존재하는지에 대한 여부, 로그인 적합성 판별 여부)


def account_exist(player_id: str) -> bool:
    # MySQL 의 Data 를 Dict 형태로 반환 시키는 DictCursor 사용
    user_db, cursor = connect_mysql()

    # 먼저, 해당 ID를 가진 유저가 있는지를 목록에서 체크해야 함. (서브 쿼리를 통해 추출)
    # 해당 ID를 가진 계정이 존재할 경우 1을 리턴, 없을 경우 0을 리턴함.
    sql = """SELECT EXISTS (SELECT * FROM playerlist 
                    WHERE playerID = %s LIMIT 1) AS 'is_exists'"""
    cursor.execute(sql, player_id)
    result = cursor.fetchone()
    user_db.close()

    return result['is_exists']


def account_login(player_id: str, player_pw: str) -> tuple[bool, str]:
    user_db, cursor = connect_mysql()
    # 해당 ID와 PW를 가진 유저 목록이 있는지를 체크해야 함.
    sql = """SELECT isConfirmed, playerPW FROM playerlist WHERE playerID = %s"""
    cursor.execute(sql, player_id)
    account_info = cursor.fetchone()
    user_db.close()

    # 먼저, 입력받은 정보에 대한 계정이 존재하는지를 체크해야 함.
    if not account_info:
        return False, '003'

    # 그 다음, 입력 받은 정보에 대한 계정이 인증되었는지를 체크해야 함.
    if not account_info['isConfirmed']:
        return False, '004'

    # DB에 내장된 값과 입력받은 PW를 암호화한 값이 동일한지를 대조.
    player_pw = player_pw.encode('utf-8')
    check_password = bcrypt.checkpw(player_pw, account_info['playerPW'].encode('utf-8'))
    # 만약 해당 PW가 서로 일치한다면 True, 일치하지 않는다면 False를 리턴.
    if check_password:
        return True, '000'
    return False, '002'


def account_register(player_id: str, player_pw: str, email: str) -> None:
    user_db, cursor = connect_mysql()

    # 새롭게 입력받은 정보를 정리하여 INSERT 로 계정을 추가함.
    sql = """INSERT INTO playerlist(playerID, playerPW, playerEmail) 
                    values (%s, %s, %s)"""
    cursor.execute(sql, (player_id, player_pw, email))
    user_db.commit()
    user_db.close()


def account_is_confirmed(email: str) -> bool:
    user_db, cursor = connect_mysql()

    # 새롭게 입력받은 정보를 정리하여 INSERT 로 계정을 추가함.
    sql = "SELECT isConfirmed FROM playerlist WHERE playerEmail = %s"
    cursor.execute(sql, email)
    is_confirmed = cursor.fetchone()
    user_db.close()

    if is_confirmed:
        return is_confirmed['isConfirmed']
    return False


def account_confirm(email: str) -> None:
    today = datetime.datetime.now()
    confirm_date = today.strftime('%Y-%m-%d')
    print(confirm_date)

    user_db, cursor = connect_mysql()

    # 새롭게 입력받은 정보를 정리하여 UPDATE 로 값을 변경함.
    sql = """UPDATE playerlist SET playerJoinDate = %s, isConfirmed = 1 WHERE playerEmail = %s;
            INSERT INTO playerstatic(playerlist_playerID) SELECT playerID FROM playerlist WHERE playerEmail = %s;
            INSERT INTO playerbest(playerlist_playerID) SELECT playerID FROM playerlist WHERE playerEmail = %s;"""
    cursor.execute(sql, (confirm_date, email, email, email))
    user_db.commit()
    user_db.close()


def account_change_password(player_id: str, player_pw: str) -> None:
    user_db, cursor = connect_mysql()

    # 새롭게 입력받은 정보를 정리하여 INSERT 로 계정을 추가함.
    sql = "UPDATE playerlist SET playerPW = %s WHERE playerID = %s"
    cursor.execute(sql, (player_pw, player_id))
    user_db.commit()
    user_db.close()


# 여기서부터는 스코어와 관련된 함수들을 작성하는 파트 (score, rank, leaderboard)
# 현재 해당 유저의 최고 점수와 최고 스테이지를 불러오는 함수
def get_user_score(player_id: str) -> dict:
    user_db, cursor = connect_mysql()

    # 해당 유저의 전체 등수, 베스트 스코어, 베스트 스테이지를 쿼리로 받아 온다.
    sql = """SELECT bestScore, bestStage FROM playerbest 
             WHERE playerlist_playerID = %s"""
    cursor.execute(sql, player_id)
    data = cursor.fetchone()
    user_db.close()

    if data:
        return data


# 현재 해당 유저의 최고 점수와 최고 스테이지, 기록 일자를 DB에 추가하는 함수
def update_user_score(player_id: str, best_score: int, best_stage: int) -> None:
    today = datetime.datetime.now()
    best_score_date = today.strftime('%Y-%m-%d')

    user_db, cursor = connect_mysql()
    sql = """UPDATE playerbest SET bestScore = %s, bestStage = %s, bestScoreDate = %s 
            WHERE playerlist_playerID = %s"""

    cursor.execute(sql, (best_score, best_stage, best_score_date, player_id))
    user_db.commit()
    user_db.close()


# 현재 해당 유저의 전체 등수를 받아오는 함수
def get_user_rank(player_id: str) -> dict:
    user_db, cursor = connect_mysql()

    # 전체 중 해당 유저의 등수를 서브 쿼리를 통해 추출하여 받아온다.
    sql = """SELECT ranking 
            FROM (SELECT playerlist_playerID, RANK() OVER (ORDER BY bestScore DESC) 'ranking' FROM playerbest) rankTBL
            WHERE rankTBL.playerlist_playerID = %s"""
    cursor.execute(sql, player_id)
    data = cursor.fetchone()
    user_db.close()

    if data:
        return data


def get_user_percent(player_id: str) -> dict:
    user_db, cursor = connect_mysql()

    # 전체 중 해당 유저의 등수를 서브 쿼리를 통해 추출하여 받아온다.
    sql = """SELECT percent FROM (SELECT playerlist_playerID, ROUND(PERCENT_RANK() OVER (ORDER BY bestScore), 4)
            AS 'percent' FROM playerbest) pctTBL WHERE pctTBL.playerlist_playerID = %s"""
    cursor.execute(sql, player_id)
    data = cursor.fetchone()
    user_db.close()

    if data:
        return 100 - data['percent'] * 100


def get_leaderboard() -> dict:
    # MySQL 의 Data 를 Dict 형태로 반환 시키는 DictCursor 사용
    user_db, cursor = connect_mysql()

    # 해당 유저의 전체 등수, 베스트 스코어, 베스트 스테이지 등을 쿼리로 받아 온다. (10명까지만)
    sql = """SELECT RANK() OVER (ORDER BY bestScore DESC) 'rank', playerlist_playerID, bestScore,
             bestStage, bestScoreDate FROM playerbest LIMIT 10"""
    cursor.execute(sql)
    data = cursor.fetchall()
    user_db.close()

    if data:
        return data


# 여기서부터는 레벨과 관련된 함수를 기입하는 곳 (레벨 업 여부, 현재 보유 경험치 및 레벨 체크)
# 현재 유저가 보유한 경험치의 수량을 얻어오는 함수.
def get_user_levelexp(player_id: str) -> dict | bool:
    # MySQL 의 Data 를 Dict 형태로 반환 시키는 DictCursor 사용
    user_db, cursor = connect_mysql()

    # 해당 유저의 전체 등수, 베스트 스코어, 베스트 스테이지 등을 쿼리로 받아 온다. (10명까지만)
    sql = """SELECT totalGetExp, totalLevel FROM playerstatic WHERE playerlist_playerID = %s"""

    cursor.execute(sql, player_id)
    data = cursor.fetchone()
    user_db.close()

    if data:
        return data
    return False


# 특정 유저에게 특정한 수량의 스타 갯수를 DB에 적용시키는 함수.
def set_user_levelexp(player_id: str, exp: int, level: int) -> None:
    # MySQL 의 Data 를 Dict 형태로 반환 시키는 DictCursor 사용
    user_db, cursor = connect_mysql()

    # 해당 유저의 전체 등수, 베스트 스코어, 베스트 스테이지 등을 쿼리로 받아 온다. (10명까지만)
    sql = """UPDATE playerstatic SET totalGetExp = %s, totalLevel = %s WHERE playerlist_playerID = %s"""

    cursor.execute(sql, (exp, level, player_id))
    user_db.commit()
    user_db.close()


# 여기서부터는 유저의 개인 정보에 대한 함수 (가입 일자, 이메일, 최고 점수 등)
# 현재 유저의 프로필을 보여주기 위해 필요한 정보를 가져오는 함수
def user_profile_info(player_id: str) -> dict:
    # MySQL 의 Data 를 Dict 형태로 반환 시키는 DictCursor 사용
    user_db, cursor = connect_mysql()

    # 해당 유저의 전체 등수, 베스트 스코어, 베스트 스테이지 등을 쿼리로 받아 온다. (10명까지만)
    sql = """SELECT pbTBL.bestScore, pbTBL.bestStage, plTBL.playerEmail,
                    plTBL.playerJoinDate, psTBL.totalGetExp, psTBL.totalLevel
            FROM playerlist plTBL
                INNER JOIN playerbest pbTBL
                    ON plTBL.playerID = pbTBL.playerlist_playerID
                INNER JOIN playerstatic psTBL
                    ON plTBL.playerID = psTBL.playerlist_playerID
            WHERE plTBL.playerID = %s"""

    cursor.execute(sql, player_id)
    data = cursor.fetchone()
    user_db.close()

    if data:
        return data

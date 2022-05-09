import json
import os
import bcrypt
import datetime
import pymysql
from pymysql import cursors

# 현재 실행 중인 파일의 절대 경로를 찾은 후, 이를 실행 경로로 설정함
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# data 파일에 저장된 mysql.json 을 로딩
with open('config/mysql.json') as myf:
    sql_config = json.load(myf)


def connect_mysql() -> tuple:
    # 수업 정보를 가져올 때마다 MySQL에 연결을 실행해야 함.
    user_db = pymysql.connect(
        host=sql_config['MYSQL_HOST'],
        user=sql_config['MYSQL_USER'],
        password=sql_config['MYSQL_PW'],
        db=sql_config['MYSQL_DB'],
        charset='utf8'
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

    return result


def account_login(player_id: str, player_pw: str) -> bool:

    user_db, cursor = connect_mysql()
    # 해당 ID와 PW를 가진 유저 목록이 있는지를 체크해야 함.
    sql = """SELECT playerPW FROM playerlist WHERE playerID = %s"""
    cursor.execute(sql, player_id)
    account_pw = cursor.fetchone()
    user_db.close()

    # 먼저, 해당 ID에 맞는 계정 정보가 존재하는지를 먼저 체크해야 한다.
    if account_pw:
        # DB에서 꺼낸 PW를 byte로 변경한 값과, 입력받은 PW를 byte로 변경한 값이 일치하는지 체크
        # 만약 해당 PW가 서로 일치한다면 True, 일치하지 않는다면 False를 리턴한다.
        player_pw = player_pw.encode('utf-8')
        check_password = bcrypt.checkpw(player_pw, account_pw['playerPW'].encode('utf-8'))
        return check_password
    return False


def account_register(player_id: str, player_pw: str, email: str) -> None:
    user_db, cursor = connect_mysql()

    # 새롭게 입력받은 정보를 정리하여 INSERT 로 계정을 추가함.
    sql = """INSERT INTO playerlist(playerID, playerPW, playerEmail) 
                    values (%s, %s, %s)"""
    cursor.execute(sql, (player_id, player_pw, email))
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
    sql = """SELECT bestScore, bestStage FROM playerlist where playerID = %s"""
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
    sql = """UPDATE playerlist SET bestScore = %s, bestStage = %s, bestScoreDate = %s WHERE playerID = %s"""

    cursor.execute(sql, (best_score, best_stage, best_score_date, player_id))
    user_db.commit()
    user_db.close()


# 현재 해당 유저의 전체 등수를 받아오는 함수
def get_user_rank(player_id: str) -> dict:
    user_db, cursor = connect_mysql()

    # 전체 중 해당 유저의 등수를 서브 쿼리를 통해 추출하여 받아온다.
    sql = """SELECT ranking
            FROM (SELECT playerID, RANK() OVER (ORDER BY bestScore DESC) 'ranking' 
                  FROM minigameweb.playerlist) ranked
            WHERE ranked.playerID = %s"""
    cursor.execute(sql, (player_id))
    data = cursor.fetchone()
    user_db.close()

    if data:
        return data


def get_leaderboard() -> dict:
    # MySQL 의 Data 를 Dict 형태로 반환 시키는 DictCursor 사용
    user_db, cursor = connect_mysql()

    # 해당 유저의 전체 등수, 베스트 스코어, 베스트 스테이지 등을 쿼리로 받아 온다. (10명까지만)
    sql = """SELECT RANK() OVER (ORDER BY bestScore DESC) 'rank', playerID, bestScore, bestStage, bestScoreDate
             FROM playerlist LIMIT 10"""

    cursor.execute(sql)
    data = cursor.fetchall()
    user_db.close()

    if data:
        return data


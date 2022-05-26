from flask import Blueprint, request, jsonify
from flask import render_template, session
from minigame.utils.database import *

main = Blueprint('main', __name__, url_prefix='/')


@main.route('/')
def main_page():
    leaderboard = get_leaderboard()
    if 'username' in session:
        username = session['username']
    return render_template("index.html", **locals())


@main.route('/minigame')
def running_game():
    username = session['username']
    total_rank = get_user_rank(username)['ranking']
    best_score, best_stage = get_user_score(username)['bestScore'], get_user_score(username)['bestStage']
    return render_template("game.html", **locals())


# minigame 화면에서 게임 결과에 대한 값을 front-end에서 받았을 때 실행.
@main.route('/minigame/result', methods=['POST'])
def get_game_result():
    username = session['username']
    # 게임 종료 후 결과 점수와 유저 개인 최고 기록을 먼저 추출함.
    result = request.get_json()
    result_score, best_score = result['currentScore'], get_user_score(username)['bestScore']

    # 먼저, (얻은 점수 / 100) 만큼의 경험치를 추가하고, 레벨이 올랐는지 체크해야 함.
    level_info = get_user_levelexp(username)
    totalLevel, totalExp = level_info['totalLevel'], level_info['totalGetExp']
    current_exp, needed_exp = totalExp + (result_score // 100), totalLevel ** 2 * 100

    # 만약 경험치를 획득한 총량이 레벨업 기준보다 높다면, 이를 반영하여 DB 수정.
    if current_exp >= needed_exp:
        set_user_levelexp(username, current_exp - needed_exp, totalLevel + 1)
    else:
        set_user_levelexp(username, current_exp, totalLevel)

    # 만약 최고 기록이 경신되었다면, DB에 새로운 값을 업데이트 해야 함
    if result_score > best_score:
        result_stage = result['currentStage']
        update_user_score(username, result_score, result_stage)

        # front-end에 새롭게 갱신할 단위가 담긴 데이터를 전송
        data = {
            'rank': "# {0}".format(get_user_rank(username)['ranking']),
            'score': "{0:,}".format(result_score),
            'stage': result_stage
        }

        # data와 정상 응답 코드인 Http 200 를 동시에 return 시킴.
        return jsonify(data), 200

    return jsonify({}), 200


@main.route('/mypage')
def my_page():
    username = session['username']

    total_rank = get_user_rank(username)['ranking']
    user_info = user_profile_info(username)

    best_score, best_stage = user_info['bestScore'], user_info['bestStage']
    playerJoinDate, playerEmail = \
        user_info['playerJoinDate'].strftime("%Y년 %m월 %d일"), user_info['playerEmail']
    totalLevel, totalExp = user_info['totalLevel'], user_info['totalGetExp']

    return render_template("mypage.html", **locals())


@main.route('/mypage/settier', methods=['POST'])
def my_tier():
    username = session['username']
    percent = get_user_percent(username)
    return jsonify({'percent': percent}), 200


@main.route('/mypage/progress', methods=['POST'])
def my_level():
    username = session['username']
    level_info = get_user_levelexp(username)
    data = {
        'level': level_info['totalLevel'],
        'exp': level_info['totalGetExp']
    }

    return jsonify(data), 200

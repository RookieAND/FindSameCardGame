from flask import Blueprint, request, jsonify
from flask import render_template, session
from minigame.utils.database \
    import (get_user_score, update_user_score, get_leaderboard, get_user_rank, star_get_amount, user_profile_info)

main = Blueprint('main', __name__, url_prefix='/')


@main.route('/')
def main_page():
    leaderboard = get_leaderboard()
    if 'username' in session:
        username = session['username']
    return render_template("index.html", **locals())


@main.route('/minigame', methods=['GET'])
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
    # 만약 최고 기록이 경신되었다면, DB에 새로운 값을 업데이트 해야 함
    if result_score > best_score:
        result_stage = result['currentStage']
        update_user_score(username, result_score, result_stage)

        # front-end에 새롭게 갱신할 단위가 담긴 데이터를 전송
        data = {
            'rank': get_user_rank(username)['ranking'],
            'score': result_score,
            'stage': result_stage
        }

        # data와 정상 응답 코드인 Http 200 를 동시에 return 시킴.
        return jsonify(data), 200


@main.route('/mypage')
def my_page():
    username = session['username']

    total_rank = get_user_rank(username)['ranking']
    total_star = star_get_amount(username)['currentStar']

    best_info = get_user_score(username)
    best_score, best_stage = best_info['bestScore'], best_info['bestStage']

    player_info = user_profile_info(username)
    playerJoinDate, playerEmail = player_info['playerJoinDate'], player_info['playerEmail']

    return render_template("mypage.html", **locals())
from flask import Blueprint, request, jsonify
from flask import render_template, session
from minigame.user_data import get_user_score, update_user_score, get_leaderboard, get_user_rank

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
    my_best = get_user_score(username)
    result_score, best_score = result['currentScore'], my_best['bestScore']
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

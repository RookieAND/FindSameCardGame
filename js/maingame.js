const startBtn = document.querySelector(".main__minigame--lobby button");
const go2LobbyBtn = document.querySelector(".main__minigame--end button");
const go2NextStageBtn = document.querySelector(".main__minigame--next-stage button");

const timeDisplay = document.querySelector('.minigame-status.time strong');
const stageDisplay = document.querySelector('.minigame-status.stage strong');
const scoreDisplay = document.querySelector('.minigame-status.score strong');

const resultStageDisplay = document.querySelector('.minigame-result.stage strong');
const resultScoreDisplay = document.querySelector('.minigame-result.score strong');

const gameStatus = document.querySelector(".main__minigame--status");
const gameLobby = document.querySelector(".main__minigame--lobby");
const gameFrame = document.querySelector(".main__minigame--main");
const gameNextStage = document.querySelector(".main__minigame--next-stage");
const gameEndLobby = document.querySelector(".main__minigame--end");

const GAME_PLAYTIME = 60000;
const GAME_BONUSTIME = 15000;

import flipCard from "./flipcard.js";

class GameStatue {
    constructor() {
        this.isGameStart = false;
        this.timeLeft = GAME_PLAYTIME;
        this.currentStage = 1;
        this.score = 0;
        this.combo = 0;
    }

    runningGame() {
        if (!this.isGameStart) {

            this.isGameStart = true;
            this.timeLeft = GAME_PLAYTIME;

            gameLobby.classList.add('started');
            gameFrame.classList.remove('not-started');
        }
    }

    prepareNextStage() {
        this.currentStage += 1;
        this.timeLeft += GAME_BONUSTIME;
        this.score += this.currentStage * 200;
        this.combo = 0;

        stageDisplay.innerText = this.currentStage;
        this.displayTimeLeft();

        gameFrame.classList.add('not-started');
        gameNextStage.classList.remove('not-completed');
    }

    runningNextStage() {
        gameFrame.classList.remove('not-started');
        gameNextStage.classList.add('not-completed');
    }

    endingGame() {
        if (this.isGameStart) {

            gameEndLobby.classList.remove('not-ended');
            gameFrame.classList.add('not-started');
            gameStatus.classList.add('ended');
    
            this.isGameStart = false;
            resultScoreDisplay.innerText = this.score.toLocaleString("en-US");
            resultStageDisplay.innerText = this.currentStage;
        }
    }

    returnToLobby() {
        gameLobby.classList.remove('started');
        gameEndLobby.classList.add('not-ended');
        gameStatus.classList.remove('ended');

        this.timeLeft = GAME_PLAYTIME;
        this.currentStage = 1;
        this.score = 0;

        scoreDisplay.innerText = this.score.toLocaleString("en-US");
        timeDisplay.innerText = "00:00"
        stageDisplay.innerText = this.currentStage;
    }

    // 현재 잔여 시간을 화면에 출력시키는 함수
    displayTimeLeft = () => {
        const timeSec = parseInt(gameObj.timeLeft / 1000);
        const timeMilliSec = gameObj.timeLeft - (timeSec * 1000);
        timeDisplay.innerText = `${String(timeSec).padStart(2, "0")}:${String(timeMilliSec).slice(0, 2).padStart(2, "0")}`;
    }

}

const gameObj = new GameStatue();
const gameCard = new flipCard(gameObj);

// 시작 버튼을 눌렀을 경우, 자동으로 게임을 실행시켜야 함.
function startGame() {

    gameObj.runningGame();
    gameCard.shuffleCard();
    gameCard.defaultCardSet();

    setTimeout(() => countTimeLeft(), 3000);
}

// 다음 스테이지를 로드하기 전에, 전처리 과정을 진행하는 함수
function gotoNextStage() {

    gameObj.runningNextStage();
    gameCard.shuffleCard();
    gameCard.defaultCardSet();

    setTimeout(() => countTimeLeft(), 3000);
}

// 현재 시간이 얼마나 흘렀는지를 체크하고, 0초라면 즉시 게임을 종료 시킴.
function checkgameStatue() {
    
    // 필드 위에 남은 카드가 0장이라면, 다음 스테이지를 로드함.
    if (gameCard.checkLeftCard() == 0) {
        setTimeout(() => gameObj.prepareNextStage(), 500);
        return true;
    }

    // 만약 시간이 초과되었다면, 게임을 종료하고 결과 창을 띄움.
    if (gameObj.timeLeft <= 0) {
        gameObj.endingGame();
        return true;
    }

    return false;
}

// 현재 시간에 따른 게임 조건을 체크하고, 0.1초씩 남은 시간을 감소시키는 함수
function countTimeLeft() {
    const gameTimeLeft = setInterval(() => {
        if (checkgameStatue()) {clearInterval(gameTimeLeft)}
        gameObj.timeLeft -= 10;
        gameObj.displayTimeLeft();
    }, 10);
}


startBtn.addEventListener('click', startGame);
go2LobbyBtn.addEventListener('click', gameObj.returnToLobby);
go2NextStageBtn.addEventListener('click', gotoNextStage);
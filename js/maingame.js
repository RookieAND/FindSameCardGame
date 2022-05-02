const startBtn = document.querySelector(".main__minigame--lobby button");
const go2LobbyBtn = document.querySelector(".main__minigame--end button");

const timeDisplay = document.querySelector('.minigame-status.time strong');

const gameStatus = document.querySelector(".main__minigame--status");
const gameLobby = document.querySelector(".main__minigame--lobby");
const gameFrame = document.querySelector(".main__minigame--main");
const gameEndLobby = document.querySelector(".main__minigame--end");

import flipCard from "./flipcard.js";
import flipCard from "./flipcard.js";

class GameStatue {
    constructor() {
        this.isGameStart = false;
        this.timeLeft = 5000;
        this.currentStage = 1;
        this.score = 0;
        this.combo = 0;
    }

    // 0.1 초 단위로 남은 숫자를 제거하며 카운트를 진행시킴
    countTimeLeft() {
        const gameTimeLeft = setInterval(() => {
            this.timeLeft -= 10;
            const {timeSec, timeMilliSec} = {timeSec : parseInt(this.timeLeft / 1000), timeMilliSec : this.timeLeft - (timeSecond * 1000)};
            timeDisplay.innerText = `${String(timeSec).padStart(2, "0")}:${String(timeMilliSec).slice(0, 2).padStart(2, "0")}`;

            if (this.timeLeft <= 0) {
                gameEnd();
                clearInterval(gameTimeLeft);
            }
        }, 10);
    }

    runningGame() {
        if (!this.isGameStart) {

            this.isGameStart = true;
            this.timeLeft = 5000;

            gameLobby.classList.add('started');
            gameFrame.classList.remove('not-started');
            // this.flipCard.defaultCardSet();
            console.log(flipCard.defaultCardSet());
        }
    }

    endingGame() {
        if (this.isGameStart) {

            gameEndLobby.classList.remove('not-ended');
            gameFrame.classList.add('not-started');
            gameStatus.classList.add('ended');
    
            this.isGameStart = false;
            this.flipCard.resetCard();
            resultScoreDisplay.innerText = this.score.toLocaleString("en-US");
        }
    }

    returnToLobby() {
        gameLobby.classList.remove('started');
        gameEndLobby.classList.add('not-ended');
        gameStatus.classList.remove('ended');
    }
}

const gameObj = new GameStatue();
const flipCard = new flipCard(gameObj);

startBtn.addEventListener('click', gameObj.runningGame());
go2LobbyBtn.addEventListener('click', gameObj.returnToLobby);
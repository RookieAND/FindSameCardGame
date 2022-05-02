const cardList = document.querySelectorAll('.main__minigame--card');
const scoreDisplay = document.querySelector('.minigame-status.score strong');

export default class flipCard {
    constructor(gameObj) {
        this.selectCard = [];
        this.lockSelect = false;
        this.gameObj = gameObj;
    }

    // 모든 카드를 순회하여 뒤집어지거나 사라졌던 카드를 원상태로 복구시키는 함수
    resetCard() {
        cardList.forEach(card => {
            if (card.classList.contains('hidden-card')) { card.classList.remove('hidden-card'); }
            if (card.classList.contains('flip-card')) { card.classList.remove('flip-card'); }
        });
    }
    
    // 선택된 서로 다른 두 카드가 동일한지를 판별하는 함수.
    checkMatchCard() {
        const isMatch = (this.selectCard[0].dataset.card === this.selectCard[1].dataset.card);
        isMatch ? hiddenMatchCard() : unfilpCard();
    }
    
    // 선택된 서로 다른 두 카드가 동일할 경우, 이를 제거하는 함수
    hiddenMatchCard(score, combo, currentStage) {
        this.selectCard.forEach(card => {
            card.removeEventListener('click', flipCurrentCard);
            setTimeout(() => card.classList.add('hidden-card'), 500);
        });
        score += (100 + combo * 10 + (currentStage - 1));
        combo += 1;
        scoreDisplay.innerText = gameObj.score.toLocaleString("en-US")
        return score, combo;
    }
    
    // 선택한 두 카드가 동일하지 않을 경우 카드를 뒤집는 함수.
    unfilpCard(combo) {
        this.lockSelect = true;
        combo = 0;
        this.selectCard.forEach(card => {
            setTimeout(() => card.classList.remove('flip-card'), 500);
        })
        this.lockSelect = false;
        return combo;
    }

    // 중복된 카드를 동일하게 선택하였을 경우, 이를 뒤집어주는 함수
    unflipCardItself() {
        this.lockSelect = true;
        setTimeout(() => this.selectCard[0].classList.remove('flip-card'), 500);
        this.lockSelect = false;
    }
    
    flipCurrentCard() {
        this.classList.add('flip-card');
        selectCard.push(this);
    
        // 아직 선택한 카드가 하나밖에 없는 경우, 해당 카드를 선택한 카드 목록에 집어넣음.
        if (selectCard.length === 1) {
            return;
        }
        let avoidCardSeleted = (selectCard[0] != selectCard[1]);
        avoidCardSeleted ? checkMatchCard() : selectCard[0].classList.remove('flip-card');
        selectCard.length = 0  
    }

    // 게임이 새롭게 시작되었을 때, 각각의 카드를 초기화하고 이벤트를 할당시킴.
    defaultCardSet() {
        cardList.forEach(card => card.addEventListener('click', flipCurrentCard));
    }
}
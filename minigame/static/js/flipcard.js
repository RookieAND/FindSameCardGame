const cardList = document.querySelectorAll('.main__minigame--card');
const scoreDisplay = document.querySelector('.minigame-status.score strong');

export default class flipCard {
    constructor(GameStatue) {
        this.selectCard = [];
        this.lockSelect = false;
        this.gameStatue = GameStatue;
    }
    
    // 선택된 서로 다른 두 카드가 동일한지를 판별하는 함수.
    checkMatchCard() {
        const isMatch = (this.selectCard[0].dataset.card === this.selectCard[1].dataset.card);
        isMatch ? this.hiddenMatchCard() : this.unfilpCard();
    }
    
    // 선택된 서로 다른 두 카드가 동일할 경우, 이를 제거하는 함수
    hiddenMatchCard = () => {
        this.selectCard.forEach(card => {
            card.removeEventListener('click', this.flipCurrentCard);
            setTimeout(() => card.classList.add('hidden-card'), 500);
        });

        // 점수 : 기본 100 점 + 콤보 ^ 2 * 10 + (스테이지 - 1) * 2 | 시간 : 0.2초 + 콤보 ^ 1.5 * 0.02초
        this.gameStatue.score += 100 + (this.gameStatue.combo ^ 2 * 10) + (this.gameStatue.currentStage - 1) * 2;
        this.gameStatue.timeLeft += 200 + (this.gameStatue.combo  ^ 1.25 * 10);
        this.gameStatue.combo += 1;

        scoreDisplay.innerText = this.gameStatue.score.toLocaleString("en-US")
    }
    
    // 선택한 두 카드가 동일하지 않을 경우 카드를 뒤집는 함수.
    unfilpCard = () => {
        // 콤보를 0으로 초기화 하고, 점수를 10점 감점시킴 (감점 시 음수라면 0으로 고정)
        this.gameStatue.combo = 0;
        this.gameStatue.score <= 10 ? this.gameStatue.score = 0 : this.gameStatue.score -= 10;
        this.selectCard.forEach(card => {
            setTimeout(() => card.classList.remove('flip-card'), 500);
        })
    }

    // 선택한 카드를 선택 목록에 넣고, 현재 상태에 따라 선택된 카드를 처리하는 함수.
    flipCurrentCard = (event) => {
        if (!this.lockSelect) {
            event.target.classList.add('flip-card');
            this.selectCard.push(event.target);

            this.lockSelect = true;
            setTimeout(() => this.lockSelect = false, 300);
    
            // 아직 선택한 카드가 하나밖에 없는 경우, 해당 카드를 선택한 카드 목록에 집어넣음.
            if (this.selectCard.length === 1) { return; }

            // 그렇지 않을 경우, 현재 선택한 카드가 같은지 다른지를 판별해야 함.
            let avoidCardSeleted = (this.selectCard[0] != this.selectCard[1]);
            avoidCardSeleted ? this.checkMatchCard() : this.selectCard[0].classList.remove('flip-card');
            this.selectCard.length = 0
        }
    }

    // 게임이 새롭게 시작되었을 때, 각각의 카드를 초기화하고 이벤트를 할당시킴.
    // + 모든 카드를 순회하여 뒤집어지거나 사라졌던 카드를 원상태로 복구시키는 함수
    defaultCardSet() {
        cardList.forEach(card => {
            card.addEventListener('click', this.flipCurrentCard);
            if (card.classList.contains('hidden-card')) { card.classList.remove('hidden-card'); }
            if (!card.classList.contains('flip-card')) { card.classList.add('flip-card'); }
        });
        // 3초 후 카드를 일괄적으로 다시 뒤집음. (잠시 보여준 후에 뒤집는 것)
        setTimeout(() =>
            cardList.forEach(card => card.classList.remove('flip-card')
            ), 3000);
    }

    shuffleCard = () => {
        const shuffleNum = [...Array(36).keys()].sort(() => Math.random() - 0.5);
        // 36개의 카드를 4분할 하여, 각 범주에 해당되는 카드를 불러와 id를 할당시킴
        // 10 스테이지 이상부터는 카드의 종류가 3개에서 6개로 늘어남.
        const cardSection = this.gameStatue.currentStage >= 10 ? 6 : 12;
        for (let i = 0; i < shuffleNum.length; i += cardSection) {
            const sameCardList = shuffleNum.slice(i, i + cardSection);
            sameCardList.forEach(cardNum => {
                cardList[cardNum].dataset.card = parseInt(i / cardSection);
            });
        }
    }

    // 현재 필드에 남은 상태에 놓인 카드가 몇 장인지를 체크하는 함수
    // 남은 카드의 수량이 0이라면 다음 스테이지로 이동하게끔 0을 리턴.
    checkLeftCard = () => {
        const leftCard = Array.from(cardList).filter(card => !card.classList.contains('hidden-card'));
        return leftCard.length;
    }
}
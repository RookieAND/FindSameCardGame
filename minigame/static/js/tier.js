const tierSection = document.querySelector(".myinfo--option.tier");
const tierIcon = document.getElementById("tier-icon");
const tierName = document.getElementById("tier-name");
const tierSpan = document.getElementById("tier-percent");
const tierPercent = document.querySelector(".myinfo--option.tier strong");

// 각 티어에 맞는 백분율, icon class, icon hex color code를 담은 객체. 
const tierInformation = {
    'bronze': {
        'percent': 70,
        'icon': 'medal',
        'color': '#CD7F32'
    },
    'silver': {
        'percent': 30,
        'icon': 'medal',
        'color': '#C0C0C0'
    },
    'gold': {
        'percent': 10,
        'icon': 'medal',
        'color': '#D4AF37'
    },
    'platinum': {
        'percent': 8,
        'icon': 'award',
        'color': '#0CBAA6'
    },
    'diamond': {
        'percent': 1,
        'icon': 'gem',
        'color': '#1289F0'
    },
    'master': {
        'percent': 0,
        'icon': 'trophy',
        'color': '#A020F0'
    },
}

// 해당 유저의 백분위에 따른 티어 디스플레이를 다르게 수정해주는 함수.
async function getScorePercentage() {
    try {
        const resultResponse = await fetch('/mypage/settier', {
            method: "POST",
            headers: {
                'Content-Type' : 'application/json',
            }
        })
        // fetch로 받아온 response를 json 형태로 변환하여 리턴
        return resultResponse.json();
    } catch (err) {
        throw new Error(err);
    }   
}

async function setPlayerTierIcon() {
    const pctResult = await getScorePercentage();
    for (const [tier, tierInfo] of Object.entries(tierInformation)) {
        if (tierInfo.percent <= pctResult['percent']) {
            const [playerTier, playerTierInfo] = [tier, tierInfo];

            tierIcon.classList.add(`fa-${playerTierInfo.icon}`);
            tierPercent.innerText = pctResult['percent'].toFixed(2);
            tierName.innerText = playerTier;

            tierSection.style.color = playerTierInfo.color;
            tierSpan.style.backgroundColor = playerTierInfo.color;
            break;
        }
    }
}

setPlayerTierIcon();
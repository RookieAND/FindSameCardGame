const progressBar = document.querySelector(".myinfo--progress");

async function getPlayerExp() {
    try {
        const resultResponse = await fetch('/mypage/progress', {
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

async function setProgressBar() {
    const prgResult = await getPlayerExp();
    const [exp, level] = Object.values(prgResult);
    
    const progress = exp / (level ** 2);
    progressBar.style.width = progress + '%';
}

setProgressBar();
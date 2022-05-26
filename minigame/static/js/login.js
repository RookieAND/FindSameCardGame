const loginForm = document.getElementById("login-form")
const loginFeedBack = document.querySelector(".check-valid");

const feedBackMsg = {
    '000': '로그인에 성공했습니다. 잠시만 기다려주세요...',
    '001':  '올바른 아이디와 비밀번호를 입력해주세요.',
    '002': '비밀번호를 잘못 입력했습니다. 다시 시도해주세요.',
    '003': '입력하신 계정은 존재하지 않는 계정입니다.',
    '004': '입력하신 계정은 이메일 인증이 되지 않았습니다.'
}

// back-end 에 formdata를 전송하고, 그에 대한 결과를 받기 위한 함수.
async function getLoginValidation() {
    try {
        const resultForm = await fetch("login/validation", {
            method: 'POST',
            redirect: 'follow',
            body: new FormData(loginForm)
        })
        return resultForm.json();
    } catch (err) {
        throw new Error(err);
    }
}

// flask 로부터 로그인이 유효한지를 체크하고, 아니라면 오류 메세지를 출력시킴.
async function checkisVaild(event) {
    event.preventDefault();
    const validResult = await getLoginValidation();

    if (validResult.result == 'fail') {
        loginFeedBack.innerText = feedBackMsg[validResult.errcode];
        return;
    }
    // 로그인에 성공했다면, 리다이렉트를 진행시킴.
    loginFeedBack.innerText = feedBackMsg['000'];
    window.location.href = validResult.url;
}

loginForm.addEventListener('submit', checkisVaild);
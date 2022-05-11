const registerSession = document.querySelector(".main__register--session");
const registerConfirm = document.querySelector(".main__register--confirm");

const registerForm = document.getElementById("register-form")
const registerConfirmForm = document.getElementById("confirm-form")

const vaildFailNotice = document.querySelector(".check-valid")


class UserRegister {
    constructor() {
        this.username = null;
        this.password = null;
        this.email = null;
    }
}


// back-end 에 formdata를 전송하고, 그에 대한 결과를 받기 위한 함수.
async function sendFormData() {
    try {
        const resultForm = await fetch("register/validation", {
            method: 'POST',
            body: new FormData(registerForm)
        })
        return resultForm.json();
    } catch (err) {
        throw new Error(err);
    }
}

// back-end 에 confirm - Formdata를 전송하고, 그에 대한 결과를 받기 위한 함수.
// 정상적으로 인증할 시 result가 success, 에러 발생 시 fail을 담은 Obj 반환.
async function sendConfirmFormData() {
    try {
        const resultForm = await fetch("register/confirm", {
            method: 'POST',
            body: new FormData(registerConfirmForm)
        })
        return resultForm.json();
    } catch (err) {
        throw new Error(err);
    }
}


// Form에 데이터를 전송한 후, 이것이 유효한지를 판별하고 classList를 수정하는 함수.
async function checkisVaild(event) {
    event.preventDefault();
    const validResult = await sendFormData();

    if (validResult.result == 'success') {
        registerSession.classList.add('submitted');
        registerConfirm.classList.remove('not-submitted');

        // userReg의 인스턴스 변수를 초기화 함.
        userReg.username = validResult.username;
        userReg.password = validResult.password;
        userReg.email = validResult.email;
        
    } else {
        vaildFailNotice.innerText = validResult.reason;
    }
}

async function checkisConfirm(event) {
    event.preventDefault();
    const confirmResult = await sendConfirmFormData();

    if (confirmResult.result == 'fail') {
        // 에러 메세지를 출력시킴 (유효 시간은 5분이라는 점을 명시)
    }
}

const userReg = new UserRegister();
registerForm.addEventListener('submit', checkisVaild);
registerConfirmForm.addEventListener('submit', checkisConfirm);
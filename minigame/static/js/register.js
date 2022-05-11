const registerSession = document.querySelector(".main__register--session");
const registerConfirm = document.querySelector(".main__register--confirm");

const registerForm = document.getElementById("register-form")


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

// Form에 데이터를 전송한 후, 이것이 유효한지를 판별하고 classList를 수정하는 함수.
async function checkisVaild(event) {
    event.preventDefault();
    const validResult = await sendFormData();

    if (validResult.result == 'success') {
        registerSession.classList.add('submitted');
        registerConfirm.classList.remove('not-submitted');
    }
}

registerForm.addEventListener('submit', checkisVaild);
const first_name = document.getElementById("first-name");
const last_name = document.getElementById("last-name");
const birth = document.getElementById("birth");
const email = document.getElementById("email");
const password1 = document.getElementById("password1");
const password2 = document.getElementById("password2");
const phone = document.getElementById("phone");
const state = document.getElementById("state");
const city = document.getElementById("city");
const zip_code = document.getElementById("zip-code");

const btn_email = document.getElementById("btn-email");
const btn_submit = document.getElementById("btn-submit");

async function checkEmail() {
    if (!regEmail(email.value)) {
        email.focus();
        return false;
    }
    email.readOnly = true;
    const data = {
        'email': email.value
    }

    $.ajax({
        type: "POST",
        url: "/api/validate-email/",
        data: data,
        datatype: "JSON",
        async: false,
        success: function (data) {
            email.value = data.email;
            if (!confirm("사용하시겠습니까?")) {
                email.readOnly = false;
                return false;
            }
            btn_email.value = "변경";
            btn_email.classList.replace('btn-secondary', 'btn-outline-secondary');
            btn_email.setAttribute("onClick", "cancelEmail()");
        },
        error: function (error) {
            alert(error.responseJSON.message);
            email.readOnly = false;
        },
    });
}


function cancelEmail() {
    email.readOnly = false;
    btn_email.innerText = "중복확인";
    btn_email.classList.replace('btn-outline-secondary', 'btn-secondary');
    btn_email.setAttribute("onClick", "checkEmail()");
}


btn_submit.addEventListener("click", async () => {
    const data = new FormData(document.getElementById("registrationForm"));
    if (validation() == false) {
        return;
    }
    email.disabled = true;
    password1.disabled = true;
    password2.disabled = true;
    state.disabled = true;
    city.disabled = true;
    zip_code.disabled = true;
    birth.disabled = true;
    btn_email.disabled = true;
    btn_submit.disabled = true;
    btn_submit.innerHTML = '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Loading...';


    $.ajax({
        type: "POST",
        headers: {
            'X-CSRFToken': csrftoken
        },
        url: "/api/registration/",
        data: data,
        enctype: "multipart/form-data", //form data 설정
        processData: false, //프로세스 데이터 설정 : false 값을 해야 form data로 인식
        contentType: false, //헤더의 Content-Type을 설정 : false 값을 해야 form data로 인식
        success: function (data) {
            location.href=data.url;
        },
        error: function (error) {
            alert(error.responseJSON.message);
            email.disabled = false;
            password1.disabled = false;
            password2.disabled = false;
            state.disabled = false;
            city.disabled = false;
            zip_code.disabled = false;
            btn_email.disabled = false;
            btn_submit.disabled = false;
        },
    });


});


//유효성 체크 함수
function validation() {
    if (first_name.value == "") {
        alert('성을 입력해주세요.');
        first_name.focus();
        return false;
    }
    if (last_name.value == "") {
        alert('이름을 입력해주세요.');
        last_name.focus();
        return false;

    }
    if (birth.value == "") {
        birth.focus();
        return false;
    }

    if (email.readOnly == false) {
        alert('이메일 중복 검사를 해주세요.');
        email.focus();
        return false;
    }

    if (password1.value != password2.value) {
        alert('비밀번호가 일치 하지 않습니다.');
        return false;
    }
    if (!regPassword(password1.value)) {
        password1.focus();
        return false;
    }
    if (phone.value.length < 10) {
        phone.focus();
        return false;
    }
    if (state.value == '') {
        state.focus();
        return false;
    }
    if (city.value == '') {
        city.focus();
        return false;
    }
    if (zip_code.value == '') {
        zip_code.focus();
        return false;
    }
    return true;
}


//이메일 정규식
function regEmail(str) {
    let reg_email = /^([0-9a-zA-Z_\.-]+)@([0-9a-zA-Z_-]+)(\.[0-9a-zA-Z_-]+){1,2}$/;

    if (!reg_email.test(str)) {
        alert('잘못된 이메일 형식입니다.');
        return false;
    }
    return true;

}

//비밀번호 정규식
function regPassword(str) {
    if (!/^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d!@#$%^&*()+.,~]{8,16}$/.test(str)) {
        alert('숫자와 영문 조합으로 8~16자리를 사용해야 합니다.');
        return false;
    }
    let checkNum = str.search(/[0-9]/g); // 숫자사용
    let checkEng = str.search(/[a-z]/ig); // 영문사용

    if (checkNum < 0 || checkEng < 0) {
        alert("숫자와 영문자를 조합하여야 합니다.");
        return false;
    }
    return true;

}

function maxLengthCheck(object) {
    if (object.value.length > object.maxLength) {
        object.value = object.value.slice(0, object.maxLength);
    }
}
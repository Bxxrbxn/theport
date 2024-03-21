const btn_login = document.getElementById("btn-login");
const email = document.getElementById('email');
const password = document.getElementById('password');

btn_login.addEventListener("click", () => {
    const data =new FormData(document.getElementById("loginForm"));
    if(!validation()){
        return false
    }
    btn_login.disabled=true;
    $.ajax({
        type: "POST",
        headers: {'X-CSRFToken': csrftoken},
        url: "",
        data: data,
        enctype: "multipart/form-data", //form data 설정
        processData: false, //프로세스 데이터 설정 : false 값을 해야 form data로 인식
        contentType: false, //헤더의 Content-Type을 설정 : false 값을 해야 form data로 인식
        success: function(data) {
            location.href = data.url;
        },
        error: function(error) {
            alert(error.responseJSON.message);
            btn_login.disabled=false;
        },
    });
});

//유효성 체크 함수
function validation(){
    if(email.value == ''){
        email.focus();
        return false;
    }
    if(password.value == ''){
        password.focus();
        return false;
    }
    return true;
}

function enterkey(event) {
    if (window.event.keyCode == 13) {
        btn_login.click()
    }
}


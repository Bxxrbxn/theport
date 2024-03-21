const new_password1 = document.getElementById("new-password1");
const new_password2 = document.getElementById("new-password2");
const btn_submit = document.getElementById("btn-submit");

btn_submit.addEventListener("click", () =>{
    const form = document.getElementById("passwordForm");
    if(!validation()){
        return false;
    }
    btn_submit.disabled = true;
    form.submit();

})


function validation(){
    let reg_password = /^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d!@#$%^&*()+.,~]{8,16}$/
    let checkNum = new_password1.value.search(/[0-9]/g); // 숫자사용
    let checkEng = new_password1.value.search(/[a-z]/ig); // 영문사용
    if(new_password1.value == ""){
        new_password1.focus();
        return false;
    }
    if(!reg_password.test(new_password1.value)){
        new_password1.focus('숫자와 영문자 조합으로 8~16자리를 사용해야 합니다.');
        return false;
    }
    if(checkNum < 0 || checkEng < 0){
        alert("")
        new_password1.focus('숫자와 영문자 조합으로 8~16자리를 사용해야 합니다.');
        return false;
    }
    if(new_password2.value == ""){
        new_password2.focus();
        return false;
    }
    if(new_password1.value != new_password2.value){
        alert("비밀번호가 일치하지 않습니다.")
        new_password2.focus();
        return false;
    }
    return true;
}


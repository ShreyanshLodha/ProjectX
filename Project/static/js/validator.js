function validator() {
    console.log("Called")
    var NameRE = /^[A-Za-z0-9 ]{3,30}$/;
    var EmailRE = /^[a-zA-Z0-9._]+@[a-zA-Z.]*[a-zA-Z]{2,}\.[a-zA-Z]{2,3}$/;
    var PhoneRE = /^[789]\d{9}$/;
    var PasswordRE = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*(_|[^\w])).{6,}$/;

    var Name = document.getElementById("name").value;
    var Email = document.getElementById("email").value;
    var Number = document.getElementById("number").value;
    var Password = document.getElementById("password").value;
    var Password1 = document.getElementById("password1").value;

    var EType = 0;
    var ErrorFlag = true;

    if (!(NameRE.test(Name))){
        EType = 1;
        ErrorFlag = false;
    }
    else if (!(EmailRE.test(Email))){
        EType = 2;
        ErrorFlag = false;
    }
    else if (!(PhoneRE.test(Number))){
        EType = 3;
        ErrorFlag = false;
    }
    else if (!(PasswordRE.test(Password))){
        EType = 4;
        ErrorFlag = false;
    }
    else if (!(Password===Password1)){
        EType = 5;
        ErrorFlag = false;
    }
    console.log(EType);
    if (EType == 1){
        alert("Name is not appropriate");
        return false;
    }
    else if(EType == 2){
        alert("Invalid EMail ID");
        return false;
    }
    else if(EType == 3){
        alert("Invalid Phone Number");
        return false;
    }
    else if(EType == 4){
        alert("Password must contain at least" +
            " 1 capital," +
            " 1 lower case character," +
            " 1 special character," +
            " 1 number" +
            "and lenght should be at least 6 ");
        return false;
    }
    else if(EType == 5){
        alert("Passwords do not match, Retry!");
        return false;
    }
}
function validator_js(){
    var today = new Date();
    var mm = today.getMonth()+1;
    var yy = today.getFullYear()
    yy = String(yy).substring(2,yy.length);

    var final_result = false;
    var card_number = document.getElementById('Card-Number').value;
    var card_exp1 = document.getElementById('Card-Exp1').value;
    var card_exp2 = document.getElementById('Card-Exp2').value;
    var amt = document.getElementById('Amount').value;
    var cvv = document.getElementById('Card-CVV').value;


    var regex_card_number = /^[0-9]{16}$/;
    var regex_cvv = /^[0-9]{3}$/;
    var regex_amt = /^[+]?([0-9]+(?:[\.][0-9]*)?|\.[0-9]+)$/;

    if(!regex_amt.test(amt)){
        document.getElementById('amount_invalid').style.display= "";
    } else if(card_exp2<=yy && mm>card_exp1) {
        document.getElementById('card_exp_invalid').style.display = "";
        if(card_exp2<yy)
            document.getElementById('card_exp_invalid').style.display = "";
    } else if(card_exp1>12 || card_exp1 <=0){
        document.getElementById('card_exp_invalid').style.display = "";
    } else if(!regex_card_number.test(card_number)){
        document.getElementById('card_number_invalid').style.display= "";
    }else if(!regex_cvv.test(cvv)){
        document.getElementById('invalid_cvv').style.display=""
    }else{
        final_result = true;
        console.log(final_result);
        document.getElementById('card_number_invalid').style.display= "none";
        document.getElementById('card_exp_invalid').style.display = "none";
        document.getElementById('amount_invalid').style.display= "none";
        document.getElementById('invalid_cvv').style.display="none"
    }

    return final_result;
}
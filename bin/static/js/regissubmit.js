function fncSubmit() {
  if(document.form1.username.value == "" || form1.username.value.length < 6 || form1.username.value.length > 12){
    alert('Please input Username and have 6 - 12 characters');
    document.form1.username.focus();
    return false;
  }
  else if(document.form1.password.value == "")  {
    alert('Please input Password');
    document.form1.password.focus();
    return false;
  }
  else if(document.form1.ConPassword.value == "")  {
    alert('Please input Confirm Password');
    document.form1.txtConPassword.focus();
    return false;
  }
  else if(document.form1.password.value != document.form1.txtConPassword.value)  {
    alert('Confirm Password Not Match');
    document.form1.txtConPassword.focus();
    return false;
  }
  else if(document.form1.accountname.value == "")  {
    alert('Please input Account Name');
    document.form1.accountname.focus();
    return false;
  }
  else if(document.form1.accountid.value == "")  {
    alert('Please input Account Num');
    document.form1.accountid.focus();
    return false;
  }
  document.form1.submit();
}

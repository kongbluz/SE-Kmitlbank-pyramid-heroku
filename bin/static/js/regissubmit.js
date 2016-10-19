function fncSubmit() {
  if(document.form1.txtUsername.value == "" || form1.txtUsername.value.length < 6 || form1.txtUsername.value.length > 12){
    alert('Please input Username and have 6 - 12 characters');
    document.form1.txtUsername.focus();
    return false;
  }
  else if(document.form1.txtPassword.value == "")  {
    alert('Please input Password');
    document.form1.txtPassword.focus();
    return false;
  }
  else if(document.form1.txtConPassword.value == "")  {
    alert('Please input Confirm Password');
    document.form1.txtConPassword.focus();
    return false;
  }
  else if(document.form1.txtPassword.value != document.form1.txtConPassword.value)  {
    alert('Confirm Password Not Match');
    document.form1.txtConPassword.focus();
    return false;
  }
  else if(document.form1.txtName.value == "")  {
    alert('Please input Account Name');
    document.form1.txtName.focus();
    return false;
  }
  else if(document.form1.txtNum.value == "")  {
    alert('Please input Account Num');
    document.form1.txtName.focus();
    return false;
  }
  document.form1.submit();
}

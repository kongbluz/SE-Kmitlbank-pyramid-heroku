function fncSubmit() {
  if(document.form1.nationid.value.length < 13) {
    alert('Nation ID is 13 characters');
    document.form1.nationid.focus();
    return false;
  }
  else if(document.form1.phonenumber.value.length < 9)  {
    alert('Phone number is between 9 - 10 characters');
    document.form1.phonenumber.focus();
    return false;
  }
  else if(document.form1.name.value == "")  {
    alert('Please input Name');
    document.form1.name.focus();
    return false;
  }
  document.form1.submit();
}

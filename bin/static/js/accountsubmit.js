function fncSubmit() {
  if(document.form1.nationid.value == "") {
    alert('Please input Nation ID and input ');
    document.form1.nationid.focus();
    return false;
  }
  else if(document.form1.phonenumber.value == "")  {
    alert('Please input phone number');
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

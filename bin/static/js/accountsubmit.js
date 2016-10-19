function fncSubmit() {
  if(document.form1.FrmIdcn.value == "" || isNaN(this.value) ) {
    alert('Please input Nation ID and input ');
    document.form1.FrmIdcn.focus();
    return false;
  }
  else if(document.form1.phone.value == "" || form1.phone.length != 10)  {
    alert('Please input phone number');
    document.form1.phone.focus();
    return false;
  }
  else if(document.form1.txtName.value == "")  {
    alert('Please input Name');
    document.form1.txtName.focus();
    return false;
  }
  document.form1.submit();
}

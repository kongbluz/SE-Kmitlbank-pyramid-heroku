function fncSubmit() {
  if(document.form1.chk1.checked == false)  {
    alert('Please Click accept');
    return false;
    }
document.form1.submit();
}

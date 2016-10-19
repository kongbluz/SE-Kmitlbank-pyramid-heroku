var day_of_week = new Array('Sun','Mon','Tue','Wed','Thu','Fri','Sat');
var month_of_year = new Array('January','February','March','April','May','June','July','August','September','October','November','December');
//  DECLARE AND INITIALIZE VARIABLES
var Calendar = new Date();
document.getElementById("demo").innerHTML = Calendar.getFullYear();     // Returns year
document.getElementById("demo1").innerHTML = month_of_year[Calendar.getMonth()];
var year = Calendar.getFullYear();     // Returns year
var month = Calendar.getMonth();    // Returns month (0-11)
var today = Calendar.getDate();    // Returns day (1-31)
var weekday = Calendar.getDay();    // Returns day (1-31)

var DAYS_OF_WEEK = 7;    // "constant" for number of days in a week
var DAYS_OF_MONTH = 31;    // "constant" for number of days in a month
var cal;    // Used for printing

Calendar.setDate(1);    // Start the calendar day at '1'
Calendar.setMonth(month);    // Start the calendar month at now

/* VARIABLES FOR FORMATTING*/
var TR_start = '<TR>';
var TR_end = '</TR>';
var highlight_start = '<TD WIDTH="20" color=777777><TABLE CELLSPACING=1 BGCOLOR=17C399 ><TR><TD WIDTH="25"><font color=white size=2 ><CENTER>';
var highlight_end   = '</CENTER></TD></TR></TABLE></font>';
var TD_start = '<TD WIDTH="45"><CENTER><font color=777777 size=2 >';
var TD_end = '</CENTER></font></TD>';
/* BEGIN CODE FOR CALENDAR */
cal =  '<TABLE BORDER=0 CELLSPACING=0 CELLPADDING=0  ><TR><TD>';
cal += '<TABLE BORDER=0 CELLSPACING=0 CELLPADDING=1>' + TR_start;
cal += TR_start;
// LOOPS FOR EACH DAY OF WEEK
// FILL IN BLANK GAPS UNTIL TODAY'S DAY
for(index=0; index < Calendar.getDay(); index++)
cal += TD_start + '  ' + TD_end;
// LOOPS FOR EACH DAY IN CALENDAR
for(index=0; index < DAYS_OF_MONTH; index++)  {
  if( Calendar.getDate() > index )  {
    week_day =Calendar.getDay();  // RETURNS THE NEXT DAY TO PRINT
    if(week_day == 0)  cal += TR_start; // START NEW ROW FOR FIRST DAY OF WEEK
    if(week_day != DAYS_OF_WEEK)  {
      var day  = Calendar.getDate();  // SET VARIABLE INSIDE LOOP FOR INCREMENTING PURPOSES
      if( today==Calendar.getDate() )  cal += highlight_start + day + highlight_end + TD_end; // HIGHLIGHT TODAY'S DATE
      else cal += TD_start + day + TD_end;  // PRINTS DAY
    }
  if(week_day == DAYS_OF_WEEK)  cal += TR_end;  // END ROW FOR LAST DAY OF WEEK
  }
  Calendar.setDate(Calendar.getDate()+1); // INCREMENTS UNTIL END OF THE MONTH
}// end for loop

//  PRINT CALENDAR
document.getElementById("demo2").innerHTML = cal.toString();
//  End -->

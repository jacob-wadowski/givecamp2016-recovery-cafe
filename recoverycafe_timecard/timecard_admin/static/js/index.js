//on ready
$(function() {
  $('#datepicker-from').datepicker({
    keyboardNavigation: false,
    autoclose: true,
    todayHighlight: true
  });

  $('#datepicker-to').datepicker({
    keyboardNavigation: false,
    autoclose: true,
    todayHighlight: true
  });

  $('#adminCheckoutTime').datetimepicker({
    format: 'yyyy-mm-dd hh:ii',
    autoclose: true,
    todayBtn: true
  });

  $('#adminCheckoutSubmit').click(function(e) {
    e.preventDefault();
    console.log($('#adminCheckoutTime').val);
  });
});

$('#myTabs a').click(function (e) {
  e.preventDefault();
  $(this).tab('show');
});

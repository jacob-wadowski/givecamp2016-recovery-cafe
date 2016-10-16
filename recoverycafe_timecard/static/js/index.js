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

  $('#myTabs a').click(function(e) {
    e.preventDefault();
    $(this).tab('show');
  });

  $('#checkinButton').click(function(e) {
    e.preventDefault();
    $.post("/timecard/post/", {
      userID: $('#userID').val(),
      event: "check in",
      branch: $('#branchSelect').val(),
      task: $('#taskSelect').val(),
      csrfmiddlewaretoken: window.CSRF_TOKEN
    }).done(function(data) {
      $('#notifName').text(data.name);
      $('#successNotification').removeClass("hidden");
    });
  });

  $("#addTask").click(function(e) {
    e.preventDefault();
    $.post('/adminView/admin/add_task/', {
      provided_task_name: $("#addTaskModal #taskName").val(),
      csrfmiddlewaretoken: window.CSRF_TOKEN
    }).done(function(data) {
        console.log(data);
    });
  });
});

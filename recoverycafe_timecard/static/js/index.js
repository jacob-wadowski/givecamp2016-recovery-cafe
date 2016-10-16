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
    $.post("/api/punchtimes", {
      volunteer_id: $('#userID').val(),
      punch_type: "IN",
      branch_id: $("#branchID").val(),
      task_id: $('#taskSelect').val(),
      flags: 0,
      csrfmiddlewaretoken: window.CSRF_TOKEN
    }).done(function(data) {
        if(data.status === "DUPLICATE" || data.status === "NO USER"){
            $('#errorMsg').text(data.msg);
            $('#failNotification').removeClass("hidden");
        }else{
            $('#notifName').text("Thank you for clocking in " + data.volunteer_id + "! Remember to clock out when you leave!");
            $('#successNotification').removeClass("hidden");
        }
        setTimeout(function(){
            //clear the user id and msgs
            $('#userID').val("");
            $('#notifName').text("");
        }, 5000);
    }).fail(function(data){
        console.log("Error: " + JSON.stringify(data));
    });
  });

  $('#checkoutButton').click(function(e) {
    e.preventDefault();
    $.post("/api/punchtimes", {
      volunteer_id: $('#userID').val(),
      punch_type: "OUT",
      branch_id: $("#branchID").val(),
      task_id: $('#taskSelect').val(),
      flags: 0,
      csrfmiddlewaretoken: window.CSRF_TOKEN
    }).done(function(data) {
        if(data.status === "NO USER"){
            $('#errorMsg').text(data.msg);
            $('#failNotification').removeClass("hidden");
        }else{
            $('#notifName').text("Thank you for clocking out " + data.volunteer_id + ". Hope to see you again soon!");
            $('#successNotification').removeClass("hidden");
        }
        setTimeout(function(){
            //clear the user id and msgs
            $('#userID').val("");
            $('#notifName').text("");
        }, 5000);
    }).fail(function(data){
        console.log("Error: " + JSON.stringify(data));
    });
  });

  $(document).on("mousedown", "#addTask", function(e) {
    e.preventDefault();
    $.post('/adminView/admin/add_task/', {
      provided_task_name: $("#addTaskModal #taskName").val(),
      csrfmiddlewaretoken: window.CSRF_TOKEN
    }).done(function(data) {
      $("#tasksTable").append("<tr><td>" + data.task_name + "</td>" + "<td style='text-align:center'><button type='button' class='btn btn-default btn-sm task-remove-btn' data-taskID='" + data.task_id + "'><span class='glyphicon glyphicon-remove' aria-hidden'true'></span</button></td></tr>");
    });
  });

  $(document).on("mousedown", ".task-remove-btn", function(e) {
    e.preventDefault();
    $.post('/adminView/admin/remove_task/', {
      button_task_id: $(this).attr("data-taskID"),
      csrfmiddlewaretoken: window.CSRF_TOKEN
    }).done(function(data) {
      elementToRemoveSelector = "#tasksTable button[data-taskID=" + data.task_id + "]";
      $(elementToRemoveSelector).closest("tr").remove();
    });
  });
});

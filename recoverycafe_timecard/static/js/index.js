//on ready
$(function() {
  $('#datepicker-from').datepicker({
    keyboardNavigation: false,
    autoclose: true,
    todayHighlight: true,
    orientation: 'bottom'
  });

  $('#datepicker-to').datepicker({
    keyboardNavigation: false,
    autoclose: true,
    todayHighlight: true,
    orientation: 'bottom'
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
      //task_id: $("#taskSelect").find("option:selected").text(),
        task_id: $("#taskSelect").val(),
      flags: 0,
      csrfmiddlewaretoken: window.CSRF_TOKEN
    }).done(function(data) {
        if(data.status === "DUPLICATE" || data.status === "NO USER"){
            $('#errorMsg').text(data.msg);
            $('#failNotification').removeClass("hidden");
        }else{
            $('#notifName').text("Thank you for clocking in " + data.volunteer.last_name + "! Remember to clock out when you leave!");
            $('#successNotification').removeClass("hidden");
        }
        //clear user id input field
        $('#userID').val("");
        setTimeout(function(){
            //clear msgs
            $('#notifName').text("");
            $('#successNotification').addClass("hidden");
            $('#failNotification').addClass("hidden");
        }, 3000);
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
      //task_name: $("#taskSelect").find("option:selected").text(),
      task_id: $("#taskSelect").val(),
      flags: 0,
      csrfmiddlewaretoken: window.CSRF_TOKEN
    }).done(function(data) {
        if(data.status === "DUPLICATE" || data.status === "NO USER"){
            $('#errorMsg').text(data.msg);
            $('#failNotification').removeClass("hidden");
        }else{
            $('#notifName').text("Thank you for clocking out " + data.volunteer.last_name + ". Hope to see you again soon!");
            $('#successNotification').removeClass("hidden");
        }
        //clear user id input field
        $('#userID').val("");
        setTimeout(function(){
            //clear msgs
            $('#notifName').text("");
            $('#successNotification').addClass("hidden");
            $('#failNotification').addClass("hidden");
        }, 3000);
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

  $('#importfile').on('change', function() {
      $('#importform').submit();
  });

    $(document).ready(function(){
        $("#importform[data-toggle='tooltip']").tooltip({
            animated: 'fade',
            placement: 'top',
            html: true
        });

        $("nav #importform[data-toggle='tooltip']").on("mouseenter", function(){
            $(this).closest("nav").find(".tooltip-inner").css({
                "background-color" : "transparent",
                "max-width" : "450px",
                /* If max-width does not work, try using width instead */
                "width" : "450px"
            });
        });

        //initialize the master list of volunteers into a datatable
        $('#volunteerMasterListTable').DataTable({
            paging: false
        });
    });

    $('#adminCheckoutButton').click(function(e) {
        var volunteerID = $(this).closest("[data-name='volunteerRow']").find("#volunteerStaffId").text();
        console.log("clicked the admin checkout button");
        console.log($(this).closest("tr").find)
        e.preventDefault();
        $.post("/api/punchtimes", {
            volunteer_id: volunteerID,
            punch_type: "OUT",
            branch_id: "1", //TODO: consider removing in checkout scenario
            task_id: "0",   //TODO: consider removing in checkout scenario
            isAdminCheckout: 1,
            adminCheckoutTime: "12:00",
            flags: 0,
            csrfmiddlewaretoken: window.CSRF_TOKEN
        }).done(function(data) {
            console.log('success');
        }).fail(function(data){
           console.log("Error: " + JSON.stringify(data));
        });
});

});

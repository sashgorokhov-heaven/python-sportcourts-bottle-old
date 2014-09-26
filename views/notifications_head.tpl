<script type="text/javascript">
  $(document).on('click', 'button', function() {
    n_id = $(this).attr("id");

    if ($('#all').hasClass('active') == true){
      var pane = 'all';
    } else if ($('#subscribed').hasClass('active') == true) {
      var pane = 'subscribed';
    } else if($('#responsible').hasClass('active') == true) {
      var pane = 'responsible';
    };

    $.ajax({
      url: '/notifications',
      data: {
      % if not all:
        read: n_id
      % end
      % if all:
        delete: n_id
      % end
      },
      async: true,
      success: function (responseData, textStatus) {
        // window.location.reload();
        var count = $(".notify").html();
        arr = $(".notify");
        count1 = count - 1;
        arr.html(count1);

        if (count1 == '0') {
          location.reload();
        }

        var count2 = $(".notify_"+pane).html();
        arr1 = $(".notify_"+pane);
        count3 = count2 - 1;
        arr1.html(count3);
      },
      error: function (response, status, errorThrown) {
      },
      type: "POST",
      dataType: "text"
    });
  });
</script>
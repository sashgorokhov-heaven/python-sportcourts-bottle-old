<script type="text/javascript">
  $(document).on('click', 'button', function() {
    n_id = $(this).attr("id");
    $.ajax({
      url: 'http://sportcourts.ru/notifications',
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
      },
      error: function (response, status, errorThrown) {
      },
      type: "POST",
      dataType: "text"
    });
  });
</script>
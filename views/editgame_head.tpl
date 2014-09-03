<script type="text/javascript">
  $(function () {
      $("#game_add_slider2").slider({
          value: {{game['duration']}},
          min: 30,
          max: 600,
          step: 10,
          slide: function (event, ui) {
              $("#game_add_long").val(ui.value + " минут");
          }
      });
      $("#game_add_long").val($("#game_add_slider2").slider("value") + " минут");
  });

  $(function () {
      $("#game_add_slider").slider({
          value: {{game['cost']}},
          min: 0,
          max: 400,
          step: 5,
          slide: function (event, ui) {
              $("#game_add_amount").val(ui.value + " руб.");
          }
      });
      $("#game_add_amount").val($("#game_add_slider").slider("value") + " руб.");
  });

  $(function () {
      $("#game_add_slider1").slider({
          value: {{game['capacity']}},
          min: 8,
          max: 40,
          step: 1,
          slide: function (event, ui) {
              $("#game_add_count").val(ui.value);
          }
      });
      $("#game_add_count").val($("#game_add_slider1").slider("value"));
  });

  $("#court").chained("#city");
</script>
<script src="/view/js/jquery.chained.js"></script>

<script>
	$(function () {
	    $("#game_add_slider").slider({
	        value: 180,
	        min: 0,
	        max: 400,
	        step: 5,
	        slide: function (event, ui) {
	            $("#game_add_amount_visible").val(ui.value + " руб.");
	            $("#game_add_amount").val(ui.value);
	        }
	    });
	    $("#game_add_amount_visible").val($("#game_add_slider").slider("value") + " руб.");
	    $("#game_add_amount").val($("#game_add_slider").slider("value"));
	});

	$(function () {
	    $("#game_add_slider1").slider({
	        value: 15,
	        min: 8,
	        max: 40,
	        step: 1,
	        slide: function (event, ui) {
	            $("#game_add_count_visible").val(ui.value);
	            $("#game_add_count").val(ui.value);
	        }
	    });
	    $("#game_add_count_visible").val($("#game_add_slider1").slider("value"));
	    $("#game_add_count").val($("#game_add_slider1").slider("value"));
	});

	function showOrHide() {
	  if($("#unlimit").is(":checked")){ 
	    $("#game_add_count").val("-1");
	    $("#game_add_slider1").slider( "disable" );
	    $("#game_add_count_visible").val("");;
	  }else{ 
	    $("#game_add_slider1").slider( "enable" );
	    $("#game_add_count_visible").val($("#game_add_slider1").slider("value"));
	    $("#game_add_count").val($("#game_add_slider1").slider("value"));
	  } 
	};

	$(function () {
	    $("#game_add_slider2").slider({
	        value: 90,
	        min: 30,
	        max: 600,
	        step: 10,
	        slide: function (event, ui) {
	            $("#game_add_long_visible").val(ui.value + " минут");
	            $("#game_add_long").val(ui.value);
	        }
	    });
	    $("#game_add_long_visible").val($("#game_add_slider2").slider("value") + " минут");
	    $("#game_add_long").val($("#game_add_slider2").slider("value"));
	});
</script>
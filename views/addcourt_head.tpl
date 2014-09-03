<script>
	$(function () {
	    $("#court_add_slider").slider({
	        range: true,
	        values: [ 1000, 1500 ],
	        min: 0,
	        max: 10000,
	        step: 50,
	        slide: function (event, ui) {
	            $("#court_add_amount").val("от " + ui.values[0] + " до " + ui.values[1] + " руб. в час");
	        }
	    });
	    $("#court_add_amount").val("от " + $("#court_add_slider").slider("values", 0) + " до " + $("#court_add_slider").slider("values", 1) + " руб. в час");
	});

	$(function () {
	    $("#court_add_slider1").slider({
	        value: 20,
	        min: 8,
	        max: 60,
	        step: 1,
	        slide: function (event, ui) {
	            $("#court_add_count").val(ui.value);
	        }
	    });
	    $("#court_add_count").val($("#court_add_slider1").slider("value"));
	});
</script>
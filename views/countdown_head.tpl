<link rel="stylesheet" type="text/css" href="/view/css/jquery.countdown.css"> 
<script type="text/javascript" src="/view/js/jquery.plugin.js"></script> 
<script type="text/javascript" src="/view/js/jquery.countdown.js"></script>
<script type="text/javascript" src="/view/js/jquery.countdown-ru.js"></script>
<script>
$(function () {
	var untilDay = new Date();
	untilDay = new Date(2014, 12, 25);
	$('#defaultCountdown').countdown({
		until: untilDay
	});
});
</script>
<style type="text/css">
#defaultCountdown {
	width: 240px;
	height: 45px;
}
</style>
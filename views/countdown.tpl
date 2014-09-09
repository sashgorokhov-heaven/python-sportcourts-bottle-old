<!DOCTYPE html>
<html>
<head>
<meta http-equiv="Content-Type" content="text/html;charset=utf-8">
<title>Счетчик</title>
<link rel="stylesheet" type="text/css" href="/view/css/jquery.countdown.css">
<style type="text/css">
#defaultCountdown { width: 240px; height: 45px; }
</style>
<script src="http://ajax.googleapis.com/ajax/libs/jquery/1.10.2/jquery.min.js"></script>
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
</head>
<body>
<h1>УУпс</h1>
<p>Здесь идут работы</p>
<p>До окончания работ</p>
<div id="defaultCountdown"></div>
</body>
</html>

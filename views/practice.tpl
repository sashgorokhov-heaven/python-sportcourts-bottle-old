<!DOCTYPE html>
<html lang="en">
<head>
	<meta charset="UTF-8">
	<title>Document</title>
	<script type="text/javascript">
		(function($) {
		    $(document).ready(function() {
		        var $panel = $('#panel');
		        if ($panel.length) {
		            var $sticker = $panel.children('#panel-sticker');
		            var showPanel = function() {
		                $panel.animate({
		                    left: '+=400',
		                }, 200, function() {
		                    $(this).addClass('visible');
		                });
		            };
		            var hidePanel = function() {
		                $panel.animate({
		                    left: '-=400',
		                }, 200, function() {
		                    $(this).removeClass('visible');
		                });
		            };
		            $sticker
		                .children('span').click(function() {
		                    if ($panel.hasClass('visible')) {
		                        hidePanel();
		                    }
		                    else {
		                        showPanel();
		                    }
		                }).andSelf()
		                .children('.close').click(function() {
		                    $panel.remove();
		                });
		        }
		    });
		})(jQuery);
	</script>
	<style>
		#panel {
		    position: absolute;
		    top: 50%;
		    left: -400px;
		    margin: -40px 0 0 0;
		    overflow: hidden;
		}
		#panel-content {
		    background: #EEE;
		    border: 1px solid #CCC;
		    width: 388px;
		    height: 80px;
		    float: left;
		    padding: 3px 5px;
		}
		#panel-sticker {
		    float: left;
		    position: relative;
		    background: orange;
		    padding: 3px 20px 3px 5px;
		    margin: 0;
		    cursor: pointer;
		}
		#panel-sticker .close {
		    position: absolute;
		    right: 3px;
		    top: 3px;
		}
	</style>
</head>
<body>
	<div id="panel">
	    <div id="panel-content">
	        Какой-то контент, который вы хотите показать.<br/>
	        Несколько строк<br/>
	        для наглядности
	    </div>
	    <div id="panel-sticker">
	        <span>Открыть</span>
	        <div class="close">×</div>    
	    </div>
	</div>
</body>
</html>
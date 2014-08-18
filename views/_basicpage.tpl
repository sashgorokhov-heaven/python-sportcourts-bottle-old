<!DOCTYPE html>
<html lang="en">
	<head>
	% include("_basichead", title=title, keywords=keywords, description=description)
  	</head>
  	<body onload="initialize_map()">
    	% include("_basicnavbar", loggedin=loggedin, user_id=user_id)
    	<div class="container theme-showcase">
			<section id="content">
				{{!base}}
			</section>
    	</div>
    	% include("_basicfooter")
  	</body>
</html>
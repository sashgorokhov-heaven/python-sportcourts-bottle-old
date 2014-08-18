<!DOCTYPE html>
<html lang="en">
	<head>
	% setdefault("keywords", 'Ключевые слова')
    % setdefault("description", 'Описание')
	% include("_basichead", title=title, keywords=keywords, description=description)
  	</head>
  	<body onload="initialize_map()">
  	    % setdefault("loggedin", False)
  	    % setdefault("user_id", 0)
    	% include("_basicnavbar", loggedin=loggedin, user_id=user_id)
    	<div class="container theme-showcase">
			<section id="content">
			    % setdefault("error_description", '')
    	        % setdefault("traceback", '')
			    % if defined('error'):
			    %   include('error_dialog', error=error, error_description=error_description, traceback=traceback)
			    % end
				{{!base}}
			</section>
    	</div>
    	% include("_basicfooter")
  	</body>
</html>
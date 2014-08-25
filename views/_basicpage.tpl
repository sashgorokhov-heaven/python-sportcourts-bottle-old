<!DOCTYPE html>
<html lang="en">
	<head>
    % setdefault("header_name", '_basichead')
	% include(header_name, title=title)
  	</head>
  	<body onload="initialize_map()">
    	% include("_basicnavbar", loggedin=loggedin, userinfo=userinfo)
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
<!DOCTYPE html>
<html lang="en">
	<head>
	% include("_basichead", title=title)
	% if defined("header_name"):
	    % include(header_name)
	% end
  	</head>
  	<body onload="initialize_map()">
    	% include("_basicnavbar", loggedin=loggedin, current_user=current_user)
    	<div class="container-fluid theme-showcase">
			<section id="content">
			    % setdefault("error_description", '')
    	        % setdefault("traceback", '')
			    % if defined('error') and error:
			    %   include('error_dialog', error=error, error_description=error_description, traceback=traceback)
			    % end
				{{!base}}
			</section>
    	</div>
    	% include("_basicfooter")
  	</body>
</html>
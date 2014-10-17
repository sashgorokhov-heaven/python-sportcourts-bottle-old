<!DOCTYPE html>
<html lang="en">
  <head>
  % include("_basichead", title=title, tplname=tplname)
  % if defined("header_name"):
      % include(header_name)
  % end
  </head>
  <body>
    % include("_basicnavbar", loggedin=loggedin, current_user=current_user, tplname=tplname)
    <div class="container theme-showcase">
    <section id="content">
        % setdefault("error_description", '')
            % setdefault("traceback", '')
        % if defined('error') and error:
        %   include('error_dialog', error=error, error_description=error_description, traceback=traceback)
        % end
      {{!base}}
    </section>
    </div>
    % include("_basicfooter", loggedin=loggedin, tplname=tplname)
  </body>
</html>
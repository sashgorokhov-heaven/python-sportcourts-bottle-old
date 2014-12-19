<!DOCTYPE html>
<html lang="en">
  <head>
  % include("_basichead")
  % if defined("header_name"):
      % include(header_name)
  % end
  </head>
  <body>
    % include("_basicnavbar")
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
    % include("_basicfooter")
    % include("_basicpostfooter")
    % if defined("footer_name"):
        % include(footer_name)
    % end
  </body>
</html>
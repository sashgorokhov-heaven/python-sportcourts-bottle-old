<!DOCTYPE html>
<html lang="en">
  <head>
  % include("_basichead", title=title)
  % if defined("header_name"):
      % include(header_name)
  % end
  <style>
    #preloader  {
         position: absolute;
         top: 0;
         left: 0;
         right: 0;
         bottom: 0;
         background-color: #fefefe;
         z-index: 99;
        height: 100%;
     }

    #status  {
         width: 200px;
         height: 200px;
         position: absolute;
         left: 50%;
         top: 15%;
         background-image: url(http://w3lessons.info/demo/jquery-preloader/ajax-loader.gif);
         background-repeat: no-repeat;
         background-position: center;
         margin: -100px 0 0 -100px;
     }
  </style>
  </head>
  <body>
    <div id="preloader">
      <div id="status">&nbsp;</div>
    </div>
    % if loggedin:
      % include("_basicnavbar", loggedin=loggedin, current_user=current_user)
    % end
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
    % include("_basicpostfooter")
    % if defined("footer_name"):
        % include(footer_name)
    % end
  </body>
</html>
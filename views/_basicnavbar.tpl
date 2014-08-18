% setdefault("loggedin", False)
% if not defined("user_id"): 
%   setdefault("user_id", 0)
%   setdefault("loggedin", False)
% end
      <div class="navbar navbar-inverse navbar-fixed-top" role="navigation">
      		<div class="container">
        		<div class="navbar-header">
            		<button type="button" class="navbar-toggle" data-toggle="collapse" data-target=".navbar-collapse">
            			<span class="sr-only">Toggle navigation</span>
            			<span class="icon-bar"></span>
            			<span class="icon-bar"></span>
            			<span class="icon-bar"></span>
          			</button>
          			<a class="navbar-brand" href="/">SportCourts Demo</a>
        		</div>
        		<div class="navbar-collapse collapse">
          			<ul class="nav navbar-nav">
          			  	<li><a class="topmenu" href="/games">Игры</a></li>
          			  	<li><a class="topmenu" href="/about">О нас</a></li>
          			  	<li><a class="topmenu" href="#" data-toggle="modal" data-target="#loginModal">Вход</a></li>
          			</ul>
        		</div>
      		</div>
    	</div>
    	<div class="container theme-showcase">
    	  <br>
    	  <p class="bg-danger" style="padding:20px;">Если вы обнаружили проблему в работе сайта, или что-то подозрительное, пожалуйста, напишите <a target="_blank" href="https://vk.com/write28638603">СЮДА</a></p>
    	</div>
	
    	<div id="footer">
    	  <div class="container">
    	    <p class="text-muted" style="margin-top: 20px;">Sportcourts. 2014</p>
    	  </div>
    	</div>
	
    	<div class="modal fade" id="loginModal" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true">
    		<div class="modal-dialog">
    		    <div class="modal-content">
    	        	<div class="modal-header">
    	        	    <button type="button" class="close" data-dismiss="modal" aria-hidden="true">&times;</button>
    	        	    <h4 class="modal-title">Авторизация</h4>
    	        	</div>
		
    	        	<div class="modal-body">
    	        	    <!-- The form is placed inside the body of modal -->
    	        	    <form id="loginForm" method="post" class="form-horizontal" autocomplete="on" action="/auth">
                            <div class="form-group" id="passwd">
                                <label class="col-sm-2 control-label">&nbsp;</label>
                                <div class="col-sm-10">
                                    <a href="https://oauth.vk.com/authorize?client_id=4436558&scope=email&redirect_uri=http://sportcourts.ru:80/auth&response_type=code&v=5.21"><img src="http://cs424830.vk.me/v424830492/6800/4W_bSTYHBEY.jpg" width="40"/></a>
                                </div>
                            </div>
    	        	        <div class="form-group" id="passwd">
    	        	            <label class="col-sm-2 control-label">Email</label>
    	        	            <div class="col-sm-10">
    	        	                <input type="email" class="form-control" name="email" data-bv-emailaddress="true"
    	        	                data-bv-notempty="true"
    	        	                data-bv-notempty-message="Введите email"/>
    	        	            </div>
    	        	        </div>
    	        	        <div class="form-group" id="passwd1">
    	        	            <label class="col-sm-2 control-label">Password</label>
    	        	            <div class="col-sm-10">
    	        	                <input type="password" class="form-control" name="password"
    	        	                data-bv-notempty="true"
    	        	                data-bv-notempty-message="Пароль обязателен и не может быть пустым"/>
    	        	            </div>
    	        	        </div>
    	        	        <div class="form-group">
    	        	            <div class="col-sm-10 col-sm-offset-2">
    	        	                <button type="submit" class="btn btn-default" name="submit_reg">Войти</button> &nbsp; или &nbsp; <a href="/registration">		Зарегистрироваться</a>
    	        	                <!--<br>
    	        	                <br>
    	        	                <a href="/recover">Восстановить пароль</a> -->
    	        	            </div>
    	        	        </div>
    	        	    </form>
    	        	</div>
    		    </div>
    		</div>
		</div>
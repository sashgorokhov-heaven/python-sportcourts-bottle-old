      % if loggedin and tplname!='index':
      <div class="container theme-showcase">
        <br>
        <div class="alert alert-danger fade in">
          <p>Если вы обнаружили проблему в работе сайта, или что-то подозрительное, пожалуйста, напишите <a target="_blank" href="https://vk.com/write28638603">СЮДА</a></p>
        </div>
      </div>
      % end
  
      <div id="footer">
        <div class="container">
          <div style="float:left;">
            <p class="text-muted">
              &copy; Sportcourts 2014
              &nbsp&nbsp&nbsp&nbsp
              <a class="topmenu" href="/about">О нас</a>
            </p>
          </div>
          <div style="float:right;">
            <p class="text-muted text-right">
              Powered by <img src="http://nichol.as/wp-content/uploads/2010/03/uwsgi.png" height=15 style="margin-bottom: 4px;">
              &nbsp
              <img src="http://bottlepy.org/docs/dev/_static/logo_nav.png" height=15 style="margin-bottom: 4px;">
            </p>
          </div>
        </div>
      </div>

      % if not loggedin:
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
                    <a href="https://oauth.vk.com/authorize?client_id=4436558&scope=email&redirect_uri=http://{{serverinfo['ip']}}:{{serverinfo['port']}}/auth&response_type=code&v=5.21">
                    <img src="/images/static/vk.png" width="32"/></a>
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
                    <button type="submit" class="btn btn-default" name="submit_reg">Войти</button> &nbsp; или &nbsp; <a href="#" data-dismiss="modal" data-toggle="modal" data-target="#regModal">Зарегистрироваться</a>
                    <br>
                    <br>
                    <a href="/recover">Восстановить пароль</a> 
                  </div>
                </div>
              </form>
            </div>
          </div>
        </div>
      </div>

      <div class="modal fade" id="regModal" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true">
        <div class="modal-dialog">
          <div class="modal-content">
            <div class="modal-header">
                <button type="button" class="close" data-dismiss="modal" aria-hidden="true">&times;</button>
                <h4 class="modal-title">Регистрация</h4>
            </div>
      
            <div class="modal-body text-center">
              <h3>Присоединяйся к сообществу спортсменов!</h3>
              <br><br>
              <div class="input-group" style="min-width:498px; margin: 0 auto;">
                <form action="" style="text-align: center">
                  <input type="text" id="email1" class="form-control input-lg" placeholder="Введи свой email" style="max-width:320px;">
                  <span class="input-group-btn">
                    <button id="email1button" class="btn btn-main btn-lg btn-success" type="submit">Присоединиться</button>
                  </span>
                </form>
                <br>
                <br>
              </div><!-- /input-group -->
            </div>
          </div>
        </div>
      </div>
      % end

      <!-- Yandex.Metrika informer --><a style="visibility:hidden;" href="https://metrika.yandex.ru/stat/?id=25660223&amp;from=informer"target="_blank" rel="nofollow"><img src="//bs.yandex.ru/informer/25660223/3_0_FFFFFFFF_FFFFFFFF_0_pageviews"style="width:88px; height:31px; border:0;" alt="Яндекс.Метрика" title="Яндекс.Метрика: данные за сегодня (просмотры, визиты и уникальные посетители)" /></a><!-- /Yandex.Metrika informer --> <!-- Yandex.Metrika counter --><script type="text/javascript"> (function (d, w, c) { (w[c] = w[c] || []).push(function() { try { w.yaCounter25660223 = new Ya.Metrika({ id:25660223, webvisor:true }); } catch(e) { } }); var n = d.getElementsByTagName("script")[0], s = d.createElement("script"), f = function () { n.parentNode.insertBefore(s, n); }; s.type = "text/javascript"; s.async = true; s.src = (d.location.protocol == "https:" ? "https:" : "http:") + "//mc.yandex.ru/metrika/watch.js"; if (w.opera == "[object Opera]") { d.addEventListener("DOMContentLoaded", f, false); } else { f(); } })(document, window, "yandex_metrika_callbacks");</script><noscript><div><img src="//mc.yandex.ru/watch/25660223" style="position:absolute; left:-9999px;" alt="" /></div></noscript><!-- /Yandex.Metrika counter -->

      % if loggedin and tplname!='index':
      <script type="text/javascript">
          var reformalOptions = {
              project_id: 798204,
              project_host: "sportcourts.reformal.ru",
              tab_orientation: "right",
              tab_indent: "50%",
              tab_bg_color: "rgb(66, 139, 202);",
              tab_border_color: "#FFFFFF",
              tab_image_url: "http://tab.reformal.ru/T9GC0LfRi9Cy0Ysg0Lgg0L%252FRgNC10LTQu9C%252B0LbQtdC90LjRjw==/FFFFFF/88128dfd6ca0743b5ccc2f8afed9f3b1/right/0/tab.png",
              tab_border_width: 1
          };
          
          (function() {
              var script = document.createElement('script');
              script.type = 'text/javascript'; script.async = true;
              script.src = ('https:' == document.location.protocol ? 'https://' : 'http://') + 'media.reformal.ru/widgets/v3/reformal.js';
              document.getElementsByTagName('head')[0].appendChild(script);
          })();
      </script><noscript><a href="http://reformal.ru"><img src="http://media.reformal.ru/reformal.png" /></a><a href="http://sportcourts.reformal.ru">Oтзывы и предложения для SportCourts</a></noscript>
      % end
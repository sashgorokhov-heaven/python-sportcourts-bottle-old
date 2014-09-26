      <div class="container theme-showcase">
        <br>
        <div class="alert alert-danger fade in">
          <p>Если вы обнаружили проблему в работе сайта, или что-то подозрительное, пожалуйста, напишите <a target="_blank" href="https://vk.com/write28638603">СЮДА</a></p>
        </div>
      </div>
  
      <div id="footer">
        <div class="container">
          <div class="row">
            <div class="col-md-6">
              <p class="text-muted" style="margin-top: 20px;">Sportcourts. 2014</p>
            </div>
            <div class="col-md-6">
              <!-- <p class="text-muted pull-right" style="margin-top: 20px;"><a class="topmenu" href="/about">О нас</a></p> -->
            </div>
          </div>
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
                    <button type="submit" class="btn btn-default" name="submit_reg">Войти</button> &nbsp; или &nbsp; <a href="/registration">   Зарегистрироваться</a>
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

      <!-- Yandex.Metrika informer --><a style="visibility:hidden;" href="https://metrika.yandex.ru/stat/?id=25660223&amp;from=informer"target="_blank" rel="nofollow"><img src="//bs.yandex.ru/informer/25660223/3_0_FFFFFFFF_FFFFFFFF_0_pageviews"style="width:88px; height:31px; border:0;" alt="Яндекс.Метрика" title="Яндекс.Метрика: данные за сегодня (просмотры, визиты и уникальные посетители)" /></a><!-- /Yandex.Metrika informer --> <!-- Yandex.Metrika counter --><script type="text/javascript"> (function (d, w, c) { (w[c] = w[c] || []).push(function() { try { w.yaCounter25660223 = new Ya.Metrika({ id:25660223, webvisor:true }); } catch(e) { } }); var n = d.getElementsByTagName("script")[0], s = d.createElement("script"), f = function () { n.parentNode.insertBefore(s, n); }; s.type = "text/javascript"; s.async = true; s.src = (d.location.protocol == "https:" ? "https:" : "http:") + "//mc.yandex.ru/metrika/watch.js"; if (w.opera == "[object Opera]") { d.addEventListener("DOMContentLoaded", f, false); } else { f(); } })(document, window, "yandex_metrika_callbacks");</script><noscript><div><img src="//mc.yandex.ru/watch/25660223" style="position:absolute; left:-9999px;" alt="" /></div></noscript><!-- /Yandex.Metrika counter -->
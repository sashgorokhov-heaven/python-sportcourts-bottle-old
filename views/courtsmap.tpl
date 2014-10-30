% rebase("_basicpage", title="Карта площадок")
        <div class="row">
          <div class="col-md-12"  style="margin-top:50px;">
            &nbsp;
          </div>
        </div>
        <div class="row">
          <div class="col-md-3">
            <div class="row">
              <div class="col-md-12 col-sm-6 col-xs-6">
                <div class="panel panel-default">
                  <div class="panel-body">
                    <p class="lead">Площадки</p>
                    <ul id="menu" style="list-style-type:none; padding-left:0;"></ul>
                    <input type="checkbox" id="hide" name="hide" value="1" onclick="YMaps.load(init)"> <small>только с играми</small>
                  </div>
                </div>
              </div>
              <div class="col-md-12 col-sm-6 col-xs-6">
                <div class="panel panel-default">
                  <div class="panel-body">
                    <p class="lead">Поделиться</p>
                    <script type="text/javascript" src="//yandex.st/share/share.js"
                    charset="utf-8"></script>
                    <div class="yashare-auto-init" data-yashareL10n="ru"
                     data-yashareQuickServices="vkontakte,facebook,twitter,odnoklassniki,gplus" data-yashareTheme="counter"></div>
                  </div>
                </div>
              </div>
            </div>
          </div>
          <div class="col-md-9">
            <div id="YMapsID" style="width: 650px; height:400px; width: 100%;"></div>
          </div>
        </div>
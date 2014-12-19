% rebase("_basicpage",title="Калькулятор")
% setdefault("showreport", False)
    <div class="row">
      <div class="col-md-12"  style="margin-top:35px;">
        &nbsp;
      </div>
    </div>
    <div class="row">
      <div class="col-md-12">
        <h1 class="h3">
          Спортивный калькулятор
          &nbsp;&nbsp;&nbsp;
          <script type="text/javascript" src="//yandex.st/share/share.js"
          charset="utf-8"></script>
          <div class="yashare-auto-init" data-yashareL10n="ru"data-yashareQuickServices="vkontakte,facebook,twitter,odnoklassniki" data-yashareTheme="counter" style="margin-left: -5px; display: inline;"></div>
        </h1>
        <hr>
      </div>
    </div>
    <div class="row" id="calculator">
      <div class="col-md-6">
        <div class="panel panel-default">
          <div class="panel-body bg-info">
            <p class="lead text-center">Входные данные</p>
            <div class="row">
              <div class="col-sm-4">
                <label for="iAge" class="control-label">Возраст</label>
                <input type="text" class="form-control" id="iAge" value="{{''}}">
              </div>
              <div class="col-sm-4">
                <label for="iWeight" class="control-label">Вес</label>
                <input type="text" class="form-control" id="iWeight">
              </div>
              <div class="col-sm-4">
                <label for="iHeight" class="control-label">Рост</label>
                <input type="text" class="form-control" id="iHeight">
              </div>
            </div>
            <br>
            <div class="row">
              <div class="col-sm-4">
                <label for="iMale" class="control-label">Пол</label>
                <select class="form-control" id="iMale">
                  <option value=""></option>
                  <option value="male">муж.</option>
                  <option value="female">жен.</option>
                </select>
              </div>
              <div class="col-sm-4">
                <label for="iAct" class="control-label">Активность</label>
                <select class="form-control" id="iAct">
                  <option value=""></option>
                  <option value="0">отсутствует</option>
                  <option value="1">легкая</option>
                  <option value="2">средняя</option>
                  <option value="3">хорошая</option>
                  <option value="4">высокая</option>
                </select>
              </div>
              <div class="col-sm-4">
                <label for="iTarget" class="control-label">Ваша цель</label>
                <select class="form-control" id="iTarget">
                  <option value=""></option>
                  <option value="0">вернуть форму</option>
                  <option value="1">похудение</option>
                  <option value="2">выносливость</option>
                  <option value="3">улучшить форму</option>
                  <option value="4">соревнования</option>
                </select>
              </div>
            </div>
            <br>
            <div class="row">
              <div class="col-sm-4">
                <label for="iWaist" class="control-label">Талия</label>
                <input type="text" class="form-control" id="iWaist">
              </div>
              <div class="col-sm-4">
                <label for="iNeck" class="control-label">Шея</label>
                <input type="text" class="form-control" id="iNeck">
              </div>
              <div class="col-sm-4">
                <label for="iHips" class="control-label">Бедра</label>
                <input type="text" class="form-control" id="iHips">
              </div>
            </div>
            <br>
            <div class="row">
              <div class="col-sm-4">
                <label for="iElbow" class="control-label">Локоть</label>
                <input type="text" class="form-control" id="iElbow">
              </div>
              <div class="col-sm-4">
                <label for="iRhr" class="control-label">Пульс в покое</label>
                <input type="text" class="form-control" id="iRhr">
              </div>
              <div class="col-sm-4">
                
              </div>
            </div>
            <!-- <div class="row">
              <div class="col-sm-12 text-center">
                <br>
                <input id="calcButton" class="btn btn-primary" value="Расчитать параметры">
              </div>
            </div> -->
          </div>
        </div>
      </div>
      <div class="col-md-6">
        <section id="results">
          <div class="panel panel-default">
            <div class="panel-body" id="pulse_body">
              <div class="row">
                <div class="col-sm-12">
                  <p class="lead text-center">Рекомендации по пульсу</p>
                  <span id="pulse_content"></span>
                </div>
              </div>
            </div>
          </div>
          <div class="panel panel-default">
            <div class="panel-body" id="mass_body">
              <div class="row">
                <div class="col-sm-12">
                  <p class="lead text-center">Состав тела</p>
                  <span id="mass_content"></span>
                </div>
              </div>
            </div>
          </div>
        </section>
      </div>
    </div>
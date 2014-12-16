% rebase("_basicpage",title="Калькулятор")
% setdefault("showreport", False)
    <div class="row">
      <div class="col-md-12"  style="margin-top:50px;">
        &nbsp;
      </div>
    </div>
    <div class="row">
      <div class="col-md-12">
        <h2 class="page-header">Спортивный калькулятор</h2>
      </div>
    </div>
    <div class="row">
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
                  <option value="0">Низкая</option>
                  <option value="1">Умеренная</option>
                  <option value="2">Высокая</option>
                </select>
              </div>
              <div class="col-sm-4"></div>
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
            <div class="row">
              <div class="col-sm-12 text-center">
                <br>
                <a id="calcButton" class="btn btn-default">Расчитать параметры</a>
              </div>
            </div>
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
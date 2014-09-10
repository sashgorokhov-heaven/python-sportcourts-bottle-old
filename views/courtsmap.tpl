% rebase("_basicpage", title="Карта площадок")
      <div class="profile">
        <!-- <div class="row">
          <div class="col-md-12">
            <p class="lead">court['title']</p>
          </div>
        </div> -->
        <div class="row">
          <div class="col-md-4">
            <div class="panel panel-default">
              <div class="panel-body">
                <p class="lead">Площадки</p>
                <div class="form-group">
                  <input type="text" class="form-control" placeholder="Поиск по спорту"></input>
                </div>
                <div class="form-group">
                  <select id="city" name="city_id" class="form-control">
                    <option value="0">Город</option>
                    <option value="1">Екатеринбург</option>
                  </select>
                </div>
                <div class="form-group">
                  <button type="button" class="btn btn-primary btn-block">Найти</button>
                </div>
                <ul id="menu" style="list-style-type:none; padding-left:0;"></ul>
              </div>
            </div>
          </div>
          <div class="col-md-8">
            <div id="YMapsID" style="width: 650px; height:400px; width: 100%;"></div>
          </div>
        </div>
      </div>
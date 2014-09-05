% rebase("_basicpage", title="Администраторская")

<div class="container">
	<div class="row clearfix">
		<div class="col-md-4 column">
		</div>
		<div class="col-md-4 column">
			<div class="page-header">
				<h1>
					Администраторская <small>Не шалить!</small>
				</h1>
			</div>
		</div>
		<div class="col-md-4 column">
		</div>
	</div>
	<div class="row clearfix">
		<div class="col-md-4 column">
		</div>
		<div class="col-md-4 column">
			<div class="row clearfix">
				<div class="col-md-4 column">
				</div>
				<div class="col-md-4 column">
					 <a id="add_city_button" href="#add_city_modal" data-toggle="modal">
					 	<button type="button" class="btn btn-default btn-block">Добавить город</button>
					 </a>
					 <br>
					 <button type="button" class="btn btn-default btn-block">Добавить спорт</button>
					 <br>
					 <button type="button" class="btn btn-default btn-block">Добавить тип игры</button>
				</div>
				<div class="col-md-4 column">
				</div>
			</div>
			
			<div class="modal fade" id="add_city_modal" role="dialog" aria-labelledby="add_city_modal_label" aria-hidden="true">
				<div class="modal-dialog">
					<div class="modal-content">
						<div class="modal-header">
							 <button type="button" class="close" data-dismiss="modal" aria-hidden="true">×</button>
							<h4 class="modal-title" id="add_city_modal_label">
								Добавить город
							</h4>
						</div>
						<div class="modal-body">
							<div class="container">
								<div class="row clearfix">
									<div class="col-md-12 column">
										<form role="form" action="/admin">
											<input type="hidden" name="action" value="add_city" />
											<div class="form-group">
												 <label for="title">Название города</label>
												 <input type="text" class="form-control" id="title" name="title" />
											</div>
											<div class="form-group">
												<div id="YMapsID" style="width:450px;height:300px;margin-top:20px;">
												</div>
                    							<input type="hidden" id="geopoint" name="geopoint"/>
											</div>
											<button type="submit" class="btn btn-default">Создать</button>
										</form>
									</div>
								</div>
							</div>
						</div>
						<div class="modal-footer">
							 <button type="button" class="btn btn-default" data-dismiss="modal">Закрыть</button>
						</div>
					</div>
				</div>
			</div>
		</div>
		<div class="col-md-4 column">
		</div>
	</div>
</div>
<script type="text/javascript">
      var map, geoResult;
      YMaps.jQuery(function () {
          map = new YMaps.Map(YMaps.jQuery("#YMapsID")[0]);
          map.addControl(new YMaps.Zoom());
      });
      function showAddress (value) {
          map.removeOverlay(geoResult);
          var geocoder = new YMaps.Geocoder(value, {results: 1, boundedBy: map.getBounds()});
          YMaps.Events.observe(geocoder, geocoder.Events.Load, function () {
              if (this.length()) {
                  geoResult = this.get(0);
                  map.addOverlay(geoResult);
                  map.setBounds(geoResult.getBounds());
                  document.getElementById('geopoint').value = this.get(0).getGeoPoint();
              }else {
                  alert("Ничего не найдено")
              }
          });
          YMaps.Events.observe(geocoder, geocoder.Events.Fault, function (geocoder, error) {
              alert("Произошла ошибка: " + error);
          })
      }
  </script>
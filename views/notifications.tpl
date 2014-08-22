% rebase("_basicpage", title="Уведомления")
			<div class="row">
				<div class="col-md-12">
					<h1>Уведомления <span class="badge">{{len(notifications}}</span></h1>
					% for notification in notifications:
					    <div class="bs-example">
					      <div class="alert alert-success fade in">
					        <button type="button" class="close" data-dismiss="alert" aria-hidden="true">notification['text']</button>
					        <strong>Уведомление</strong> Плохое.
					      </div>
					    </div>
					% end
					<div class="bs-example">
					  <div class="alert alert-danger fade in">
					    <button type="button" class="close" data-dismiss="alert" aria-hidden="true">&times;</button>
					    <strong>Уведомление</strong> Хорошее.
					  </div>
					</div>
				</div>
			</div>
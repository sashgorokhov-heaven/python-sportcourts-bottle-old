% rebase("_basicpage", title="Тест")

<div class="jumbotron">
    <div class="row">
        <form id="registrationForm" method="post" class="form-horizontal" action="/widget"
        enctype="multipart/form-data">
            <script type="text/javascript">
                $('.fileinput').fileinput()
            </script>

            <div class="fileinput fileinput-new" data-provides="fileinput">
              <div class="fileinput-preview thumbnail" data-trigger="fileinput" style="width: 200px; height: 200px;">
              </div>
              <div>
                <span class="btn btn-default btn-file">
                <span class="fileinput-new">Select image</span>
                <span class="fileinput-exists">Change</span>
                <input type="file" name="avatar"></span>
                <a href="#" class="btn btn-default fileinput-exists" data-dismiss="fileinput">Remove</a>
              </div>
            </div>

            <div class="form-group">
              <div class="col-sm-offset-2 col-sm-8" style="text-align:center;">
                <button type="submit" class="btn btn-primary">Зарегистрироваться</button>
              </div>
            </div>
        </form>
    </div>
</div>
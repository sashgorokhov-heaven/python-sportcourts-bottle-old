% rebase("_adminpage", title="Админка")
% import datetime
<form id="data" method="post" action="/blog/add">
  <div class="row">
    <div class="col-md-8">
      <textarea id="textcontent" name="content" style="width:100%; height: 65vh;"></textarea>
    </div>
    <div class="col-md-4">
      <div class="form-group">
        <p class="lead">Автор: <a href="/profile/{{current_user.user_id()}}">{{current_user.name}}</a></p>
      </div>
      <div class="form-group">
        <input type="text" class="form-control" name="title" placeholder="Заголовок статьи" value=""
        data-bv-notempty="true"
        data-bv-notempty-message="Название не может быть пустым"/>
        <span id="valid"></span>
      </div>
      <div class="form-group">
        <select data-placeholder="Выберите разделы для статьи"  multiple="multiple" class="form-control chosen-select chosen-select-1" tabindex="-1" name="tag">
          % for tag in tags:
            <option value="{{tag.tag_id()}}">{{tag.title()}}</option>
          % end
        </select>
        <script>
          $(".chosen-select").chosen({
            disable_search: true,
            max_selected_options: 5
          });
        </script>
        <span id="valid"></span>
      </div>
      <a class="btn btn-success" id="submittext" type="submit">Отправить</a>
    </div>
  </div>
</form>


<script type="text/javascript">
tinymce.init({
    selector: "textarea",
    theme: "modern",
    plugins: [
        "autolink lists link image charmap preview hr anchor pagebreak",
        "wordcount code",
        "insertdatetime media nonbreaking save table directionality",
        "emoticons paste autosave"
    ],
    menubar : false,
    toolbar1: "undo redo | preview | styleselect | bullist numlist | link image media emoticons | table charmap | code",
    image_advtab: true,
    templates: [
        {title: 'Test template 1', content: 'Test 1'},
        {title: 'Test template 2', content: 'Test 2'}
    ],
    pagebreak_separator: "<!-- my page break -->"
});

$(document).on('click','#submittext',function(){

    var value = tinyMCE.get('textcontent').getContent();

    $.ajax({
      url: '/blog/add',
      data: {
        text: value
      },
      async: true,
      success: function (responseData, textStatus) {
        alert('Success');
      },
      error: function (response, status, errorThrown) {
        alert('Error \n\r\n\r' + response + '\n\r' + status + '\n\r' + errorThrown);
      },
      type: "POST",
      dataType: "text"
    });

});
</script>
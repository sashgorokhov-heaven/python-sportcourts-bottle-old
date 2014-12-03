% rebase("_adminpage", title="Админка")

<form id="data" method="post" action="">
    <textarea id="textcontent" name="content" style="width:100%; height: 65vh;"></textarea>
</form>
<br>
<a class="btn btn-lg btn-success" id="submittext">Отправить</a>

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
    alert(value);

});
</script>
<script src="/view/js/fuse.min.js"></script>

<script>
  function inittable() {
    for (var i = 1; i < 30; i++) {
      $('#articlestable').append('<tr class="success"><td>'+i+'</td><td><a href="/blog/'+i+'" target="_blank">Mad Bounce 2</a></td><td><a href="/profile/1" target="_blank">Виталий Харченко</a></td><td><div class="btn-group"><button type="button" class="btn btn-default btn-xs dropdown-toggle" data-toggle="dropdown">Действие <span class="caret"></span></button><ul class="dropdown-menu" role="menu"><li><a>Опубликовать</a></li><li><a>Отправить на перепись</a></li></ul></div></td></tr>');
    }
  };

  $(document).ready(function() {
    inittable();
  });
</script>
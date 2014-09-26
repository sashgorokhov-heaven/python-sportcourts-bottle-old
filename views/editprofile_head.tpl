<link rel="stylesheet" href="/view/jasny/css/jasny-bootstrap.css">
<script src="/view/jasny/js/jasny-bootstrap.js"></script>

<script type="text/javascript">
    $('.fileinput').fileinput()
</script>

<script type="text/javascript">
  $('.typeahead').typeahead({
    source: [{{!', '.join(['"{}"'.format(i['title']) for i in cities])}}],
    items: {{len(cities)}},
    minLength: 1
  })
</script>

<script type="text/javascript">
  $('.phonemask').inputmask({
    mask: '+7 (999) 999 99 99'
  })
</script>
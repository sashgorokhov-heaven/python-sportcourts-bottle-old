<script>
  $(document).ready(function(){

    var startFromNew = 0;

    var oldUsers = $('.user').size();

    $('#more').click(function() {

      $("#userstable").append(
        '<tr>
          <td>' + (oldUsers+startFromNew+1) + '</td>
          <td>Имя</td>
          <td>Фамилия</td>
          <td>Телефон</td>
          <td>
            <select class="form-control">
              <option value="0"></option>
              <option value="1">Оплатил</option>
              <option value="2">Не оплатил</option>
              <option value="3">Не пришел</option>
            </select>
          </td>
          <td>Подпись</td>
        </tr>'
      );

      startFromNew += 1;
    });
  });
</script>
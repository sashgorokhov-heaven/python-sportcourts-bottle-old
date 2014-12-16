<script>
  function validate(arr) {
    var age = arr['age'],
    weight = parseFloat(arr['weight']),
    height = parseFloat(arr['height']),
    male = arr['male'],
    neck = parseFloat(arr['neck']),
    hips = parseFloat(arr['hips']),
    waist = parseFloat(arr['waist']);

    var val_flag = true;

    if (height < 100 || height > 250) { 
      alert("Введите правильный рост");
      val_flag = false;
    };

    if (weight < 25 || weight > 250) { 
      alert("Введите правильный вес");
      val_flag = false;
    };

    return val_flag;
  }

  function calculate () {
    arr = [];
    arr = getparams();

    is_validate = validate(arr);

    if (is_validate) {

      var age = arr['age'],
      weight = parseFloat(arr['weight']),
      height = parseFloat(arr['height']),
      male = arr['male'],
      neck = parseFloat(arr['neck']),
      hips = parseFloat(arr['hips']),
      waist = parseFloat(arr['waist']);

      arr['pulse_1'] = 220 - age;
      arr['pulse_2'] = 150 - age;
      arr['pulse_3'] = 190 - age;

      if(!age) {
        arr['pulse_flag'] = false;
      } else {
        arr['pulse_flag'] = true;
      }

      arr['mass_1'] = (weight/height/height*100*100).toFixed(2);
      arr['mass_2'] = (waist/height).toFixed(2);

      logcon = Math.LN10;
      if (male == 'male') {
        arr['mass_3'] = (495/(1.0324 - 0.19077*(Math.log(waist-neck)/logcon) + 0.15456*(Math.log(height)/logcon) ) - 450).toFixed(2);
      } else {
        arr['mass_3'] = (495/(1.29579 - 0.35004*(Math.log(waist+hips-neck)/logcon) + 0.22100*(Math.log(height)/logcon) ) - 450).toFixed(2);
      };

      if(!waist || !male || !neck || !height || !arr['mass_1'] || !arr['mass_2'] || !arr['mass_3']) {
        arr['mass_flag'] = false;
      } else {
        arr['mass_flag'] = true;
      }

      return arr;
    } else {
      return false;
    };
  };

  function getparams () {
    var result = [];

    result['age'] = $('#iAge').val();
    result['weight'] = $('#iWeight').val();
    result['height'] = $('#iHeight').val();
    result['male'] = $('#iMale').val();
    result['waist'] = $('#iWaist').val();
    result['neck'] = $('#iNeck').val();
    result['hips'] = $('#iHips').val();

    return result;
  };

  function writeresults (arr) {
    if (arr['pulse_flag']) {
      $('#pulse_content').html('<p>Критическая частота сердцебиения: <span id="pulse_1"></span> уд/мин</p><p>Диапазон частот для кардионагрузки: от <span id="pulse_2"></span> до <span id="pulse_3"></span> уд/мин</p>');
      $('#pulse_1').html(arr['pulse_1']);
      $('#pulse_2').html(arr['pulse_2']);
      $('#pulse_3').html(arr['pulse_3']);
      $('#pulse_body').addClass('bg-success');
    } else {
      $('#pulse_content').html('<p>Для подсчета рекомендаций укажите, пожалуйста, свой возраст.</p>');
      $('#pulse_body').removeClass('bg-success');
    }

    if (arr['mass_flag']) {
      $('#mass_content').html('<p>Индекс массы тела: <span id="mass_1"></span></p><p>Отношение талии к высоте: <span id="mass_2"></span></p><p>Процент жира в организме: <span id="mass_3"></span>%</p>');
      $('#mass_1').html(arr['mass_1']);
      $('#mass_2').html(arr['mass_2']);
      $('#mass_3').html(arr['mass_3']);
      $('#mass_body').addClass('bg-success');
    } else {
      var str = '';
      if (!arr['height']){
        str += ' ,рост';
      }
      if (!arr['waist']){
        str += ', обхват талии';
      }
      if (!arr['hips']){
        str += ', обхват бедер';
      }
      if (!arr['neck']){
        str += ', обхват шеи';
      }
      str = str.slice(2);
      str += '.';
      $('#mass_content').html('<p>Для подсчета рекомендаций укажите: '+str+'</p>');
      $('#mass_body').removeClass('bg-success');
    }
  };

  function showresults () {
    $('#results').show();
  };

  function hideresults () {
    $('#results').hide();
  };

  $(document).on('click','#calcButton',function(){
    arr = calculate();
    console.log('Посчитали');
    console.log(arr);
    if (arr) {
      writeresults(arr);
    };
    showresults();
  });

  $(document).ready(function() {
    hideresults();
    % if loggedin:
      % if user.height() > 0:
      $('#iHeight').val('{{user.height()}}')
      % end
      % if user.weight() > 0:
      $('#iWeight').val('{{user.weight()}}')
      % end
      % if user.bdate():
      $('#iAge').val('{{user.bdate.age}}')
      % end
      % if user.sex() == 'female':
      $('#iMale :last').attr("selected", "selected");
      console.log('баба');
      % end
    % end
  });
</script>
<script>
  // проверяет величины на абсурдность
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

  //считает необходимые величины
  function calculate () {
    arr = [];
    arr = getparams();

    is_validate = validate(arr);

    //считаем только неабсурдные данные
    if (is_validate) {

      var age = arr['age'],
      weight = parseFloat(arr['weight']),
      height = parseFloat(arr['height']),
      male = arr['male'],
      activity = arr['activity'],
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

      if(height && weight) {
        arr['mass_imt'] = (weight/height/height*100*100).toFixed(2);
      };
      if(waist) {
        arr['mass_2'] = (waist/height).toFixed(2);
      }

      logcon = Math.LN10;
      if (male == 'male') {
        if (waist && neck && height) {
          arr['mass_fat'] = (495/(1.0324 - 0.19077*(Math.log(waist-neck)/logcon) + 0.15456*(Math.log(height)/logcon) ) - 450).toFixed(2);
          arr['mass_calmin'] = Math.floor(1842 + (height-150)*15.4 + .5);
          arr['mass_calmax'] = Math.floor(2488 + (height-150)*23.6 + .5);
        };
      } else if (male == 'female') {
        if (waist && neck && height && hips) {
          arr['mass_fat'] = (495/(1.29579 - 0.35004*(Math.log(waist+hips-neck)/logcon) + 0.22100*(Math.log(height)/logcon) ) - 450).toFixed(2);
          arr['mass_calmin'] = Math.floor(1622 + (height-150)*13.2 + .5);
          arr['mass_calmax'] = Math.floor(2194 + (height-150)*19.3 + .5);
        };
      };

      if (activity == '0') {
        var mass_protein_per = 0.8;
      } else if (activity == '1') {
        var mass_protein_per = 1.1;
      } else if (activity == '2') {
        var mass_protein_per = 1.4;
      };

      arr['mass_protein'] = Math.floor(mass_protein_per * (25 * height * height / 10000));
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
    result['activity'] = $('#iAct').val();
    result['waist'] = $('#iWaist').val();
    result['neck'] = $('#iNeck').val();
    result['hips'] = $('#iHips').val();
    result['activity'] = $('#iAct').val();

    return result;
  };

  function writeresults (arr) {
    console.log(arr);

    if (arr['pulse_flag']) {
      $('#pulse_content').html('<p>Критическая частота сердцебиения: <span id="pulse_1"></span> уд/мин</p><p>Диапазон частот для кардионагрузки: от <span id="pulse_2"></span> до <span id="pulse_3"></span> уд/мин</p>');
      $('#pulse_1').html(arr['pulse_1']);
      $('#pulse_2').html(arr['pulse_2']);
      $('#pulse_3').html(arr['pulse_3']);
      $('#pulse_body').addClass('bg-success');
    } else {
      $('#pulse_content').html('<p>Для подсчета рекомендаций укажите, пожалуйста, свой возраст.</p>');
      $('#pulse_body').removeClass('bg-success');
    };

    // работаем с аудитом массы
    var mass_err_flag = false;

    // смотрим недостающие величины, формируем рекомендацию
    var mass_err_str = '';
    if (!arr['weight']) { mass_err_str += ', массу'; };
    if (!arr['height']) { mass_err_str += ', рост'; };
    if (!arr['male']) { mass_err_str += ', пол'; };
    if (!arr['activity']) { mass_err_str += ', уровень активности'; };
    if (!arr['waist']){ mass_err_str += ', обхват талии'; };
    if (!arr['hips']){ mass_err_str += ', обхват бедер'; };
    if (!arr['neck']){ mass_err_str += ', обхват шеи'; };
    if (mass_err_str){
      mass_err_str = mass_err_str.slice(2);
      mass_err_str = '<br><small><p>*Для полной рекомендации укажите: ' + mass_err_str;
      mass_err_str += '.</p></small>';
    }

    // формируем отчет по ИМТ
    if (arr['mass_imt']) {
      var mass_imt_msg = '';
      mass_imt_msg += '<p>Индекс массы тела: <strong>' + arr['mass_imt']
      mass_imt_msg += '</strong> <small>(';
      if (arr['mass_imt'] <= 18.5) {
        mass_imt_msg += 'наблюдается дефицит массы тела';
      } else if (arr['mass_imt'] <= 25) {
        mass_imt_msg += 'у вас нормальная масса тела';
      } else if (arr['mass_imt'] <= 30) {
        mass_imt_msg += 'у вас наблюдается избыточная масса';
      } else {
        mass_imt_msg += 'угроза ожирения';
      };
      mass_imt_msg += ')</small>';
    } else {
      var mass_imt_msg = '';
      mass_err_flag = true;
    };

    // формируем отчет по отношению
    if (arr['mass_2']) {
      var mass_2_msg = '';
      mass_2_msg += '<p>Отношение талии к высоте: <strong>' + arr['mass_2']
      mass_2_msg += '</strong> <small>(';
      if (arr['mass_2'] <= 0.5) {
        mass_2_msg += 'норма';
      } else {
        mass_2_msg += 'повышенное количество брюшного жира';
      };
      mass_2_msg += ')</small>';
    } else {
      var mass_2_msg = '';
      mass_err_flag = true;
    };

    // формируем отчет по проценту жира
    if (arr['mass_fat']) {
      var mass_fat_msg = '';
      mass_fat_msg += '<p>Процент жира в организме: <strong>' + arr['mass_fat'] + '%</strong>';
      mass_fat_msg += ' <small>(';
      if (arr['male'] == 'male') {
        if (arr['mass_fat'] <= 0) {
          mass_fat_msg += 'анарексия';
        } else if (arr['mass_fat'] <= 4) {
          mass_fat_msg += 'сухое тело';
        } else  if (arr['mass_fat'] <= 13) {
          mass_fat_msg += 'спортивное телосложение';
        } else  if (arr['mass_fat'] <= 18) {
          mass_fat_msg += 'нормальное телосложение';
        } else  if (arr['mass_fat'] <= 25) {
          mass_fat_msg += 'приемлимая полнота';
        } else {
          mass_fat_msg += 'болезненная полнота';
        };
      } else if (arr['male'] == 'female') {
        if (arr['mass_fat'] <= 0) {
          mass_fat_msg += 'анарексия';
        } else if (arr['mass_fat'] <= 12) {
          mass_fat_msg += 'сухое тело';
        } else  if (arr['mass_fat'] <= 20) {
          mass_fat_msg += 'спортивное телосложение';
        } else  if (arr['mass_fat'] <= 25) {
          mass_fat_msg += 'нормальное телосложение';
        } else  if (arr['mass_fat'] <= 32) {
          mass_fat_msg += 'приемлимая полнота';
        } else {
          mass_fat_msg += 'болезненная полнота';
        };
      };
      mass_fat_msg += ')</small>';
    } else {
      var mass_fat_msg = '';
      mass_err_flag = true;
    };

    // формируем отчет по калориям
    if (arr['mass_calmin'] && arr['mass_imt']) {
      var mass_cal_msg = '';
      mass_cal_msg += '<p>Минимальное число калорий: <strong>' + arr['mass_calmin'] + ' ккал в день';
      mass_cal_msg += '</strong>';
      if (arr['mass_imt'] >= 30) {
        mass_cal_msg += '<small><p>Ограничьте Вашу диету ' + Math.floor(arr['mass_calmin']*0.75) + ' ккалл в день, чтобы терять ' + Math.floor(arr['mass_calmin']*0.25*30/4086/2.2) + ' кг в месяц</p>';
      } else if (arr['mass_imt'] >= 25) {
        mass_cal_msg += '<small><p>Ограничьте Вашу диету ' + Math.floor(arr['mass_calmin']*0.85) + ' ккалл в день, чтобы терять ' + Math.floor(arr['mass_calmin']*0.15*30/4086/2.2) + ' кг в месяц</p>';
      } else {
        mass_cal_msg += '';
      };
    } else {
      var mass_cal_msg = '';
      mass_err_flag = true;
    };

    // формируем отчет по белку
    if (arr['mass_protein']) {
      var mass_protein_msg = '';
      mass_protein_msg += '<p>Потребляйте примерно <strong>' + arr['mass_protein'] + ' г. белка в день</strong> <small>(' + (arr['mass_protein']/arr['weight']).toFixed(2) + ' грамм на кг.)</small>';
    } else {
      var mass_protein_msg = '';
      mass_err_flag = true;
    };

    if (!mass_imt_msg && !mass_2_msg && !mass_fat_msg && !mass_cal_msg && !mass_protein_msg) {
      mass_err_str = '<p>Недостаточно данных</p>' + mass_err_str;
    };

    $('#mass_content').html(mass_imt_msg+mass_2_msg+mass_fat_msg+mass_cal_msg+mass_protein_msg+mass_err_str);
    $('#mass_2').html(arr['mass_2']);
    $('#mass_3').html(arr['mass_3']);
    if (!mass_err_flag) {
      $('#mass_body').addClass('bg-success');
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
    if (arr) {
      writeresults(arr);
    };
    showresults();
  });

  $(document).ready(function() {
    % if loggedin:
      % if user.height() > 0:
      $('#iHeight').val('{{user.height()}}')
      % end
      % if user.weight() > 0:
      $('#iWeight').val('{{user.weight()}}')
      % end
      % if user.bdate():
      $('#iAge').val('{{(user.bdate.age-1)}}')
      % end
      % if user.sex() == 'female':
      $('#iMale>option[value="female"]').attr("selected", "selected");
      % end
      % if user.sex() == 'male':
      $('#iMale>option[value="male"]').attr("selected", "selected");
      % end
    % end
    arr = calculate();
    if (arr) {
      writeresults(arr);
    };
  });
</script>
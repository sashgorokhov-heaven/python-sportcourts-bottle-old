<meta property="og:title" content="Спортивный калькулятор" />
<meta property="og:site_name" content="SportCourts.ru" />
<meta property="og:type" content="website" />
<meta property="og:url" content="http://{{serverinfo['ip']}}:{{serverinfo['port']}}/calc"/>
<meta property="og:image" content="/images/static/calc.jpg" />
<meta property="og:description" content="Проверьте свое тело и получите рекомендации по тренировкам!"/>

<script>
  // проверяет величины на абсурдность
  function validate(arr) {
    var age = arr['age'],
    weight = parseFloat(arr['weight']),
    height = parseFloat(arr['height']),
    male = arr['male'],
    neck = parseFloat(arr['neck']),
    hips = parseFloat(arr['hips']),
    waist = parseFloat(arr['waist']),
    elbow = parseFloat(arr['elbow']);
    activity = parseInt(arr['activity']);
    rhr = parseFloat(arr['rhr']);

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
      target = arr['target'],
      neck = parseFloat(arr['neck']),
      hips = parseFloat(arr['hips']),
      waist = parseFloat(arr['waist']);
      elbow = parseFloat(arr['elbow']);
      rhr = parseFloat(arr['rhr']);

      if (age) {
        arr['pulse_1'] = 220 - age;
        arr['pulse_2'] = 150 - age;
        arr['pulse_3'] = 190 - age;
      };

      if (target && age && rhr) {
        var koef = 0.5 + (0.1 * target);
        arr['pulse_min'] = Math.floor(((220 - age - rhr) * koef) + rhr * 1);
        arr['pulse_max'] = Math.floor(((220 - age - rhr) * (koef + 0.1)) + rhr * 1);
      };

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
      } else if (activity <= '2') {
        var mass_protein_per = 1.1;
      } else if (activity <= '4') {
        var mass_protein_per = 1.4;
      };

      if (activity && height) {
        arr['mass_protein'] = Math.floor(mass_protein_per * (25 * height * height / 10000));
      };

      var mass_sizes = Array("хрупкое", "нормальное", "крупное");

      if (male == 'male' && height && elbow) {
        if (height < 162) {
          if (elbow < 6.35) { var mass_size = mass_sizes[0]; }
          else if (elbow > 7.28) { var mass_size = mass_sizes[2]; }
          else { var mass_size = mass_sizes[1]; };
        } else if (height < 172) {
          if (elbow < 6.65) { var mass_size = mass_sizes[0]; }
          else if (elbow > 7.28) { var mass_size = mass_sizes[2]; }
          else { var mass_size = mass_sizes[1]; };
        } else if (height < 182) {
          if (elbow < 6.98) { var mass_size = mass_sizes[0]; }
          else if (elbow > 7.62) { var mass_size = mass_sizes[2]; }
          else { var mass_size = mass_sizes[1]; };
        } else if (height < 192) {
          if (elbow < 6.98) { var mass_size = mass_sizes[0]; }
          else if (elbow > 7.92) { var mass_size = mass_sizes[2]; }
          else { var mass_size = mass_sizes[1]; };
        } else if(height < 202) {
          if (elbow < 7.28) { var mass_size = mass_sizes[0]; }
          else if (elbow > 8.25) { var mass_size = mass_sizes[2]; }
          else { var mass_size = mass_sizes[1]; };
        } else {
          if (elbow < 7.45) { var mass_size = mass_sizes[0]; }
          else if (elbow > 8.5) { var mass_size = mass_sizes[2]; }
          else { var mass_size = mass_sizes[1]; };
        };
      } else if (male == 'female' && height && elbow) {
        if (height < 162) {
          if (elbow < 5.71) { var mass_size = mass_sizes[0]; }
          else if (elbow > 6.35) { var mass_size = mass_sizes[2]; }
          else { var mass_size = mass_sizes[1]; };
        } else if(height > 180) {
          if (elbow < 6.35) { var mass_size = mass_sizes[0]; }
          else if (elbow > 6.98) { var mass_size = mass_sizes[2]; }
          else { var mass_size = mass_sizes[1]; };
        } else {
          if (elbow < 6.02) { var mass_size = mass_sizes[0]; }
          else if (elbow > 6.65) { var mass_size = mass_sizes[2]; }
          else { var mass_size = mass_sizes[1]; };
        };
      };

      arr['mass_size'] = mass_size;

      if (waist && hips) {
      var WtHR = Math.round(waist / hips * 100);
        var body_shape = '';
        if (male == 'male')
          if(WtHR <= 95)
            body_shape = ', грушевидное.';
          else
            body_shape = ', "яблоко"';
        else if (male == 'female')
          if(WtHR <= 80)
            body_shape = ', грушевидное.';
          else
            body_shape = ', "яблоко"';
      };

      // arr['mass_form'] = body_shape;

      if (weight && height && age) {
        arr['mass_rmr'] = (66 + (6.23 * (weight * 2.2)) + (12.7 * (height / 2.54)) - (6.8 * age)).toFixed(0);
      };

      if (arr['mass_rmr'] && activity) {
        var activity_factor = Array(1.3, 1.4, 1.55, 1.725, 1.9);
        arr['mass_aam'] = (arr['mass_rmr'] * activity_factor[activity]).toFixed(0);
      };

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
    result['elbow'] = $('#iElbow').val();
    result['activity'] = $('#iAct').val();
    result['target'] = $('#iTarget').val();
    result['rhr'] = $('#iRhr').val();

    return result;
  };

  function writeresults (arr) {
    console.log(arr);

    var pulse_err_flag = false;

    // смотрим недостающие величины, формируем рекомендацию
    var pulse_err_str = '';
    if (!arr['age']) { pulse_err_str += ', возраст'; };
    if (!arr['target']) { pulse_err_str += ', цели занятия спортом'; };
    if (!arr['rhr']) { pulse_err_str += ', пульс в покое'; };
    if (pulse_err_str){
      pulse_err_str = pulse_err_str.slice(2);
      pulse_err_str = '<br><small><p>*Для полной рекомендации укажите: ' + pulse_err_str;
      pulse_err_str += '.</p></small>';
    }

    if (arr['pulse_1'] && arr['pulse_2'] && arr['pulse_3']) {
      var pulse_1_msg = '<p>Критическая частота сердцебиения: '+arr['pulse_1']+' уд/мин</p><p>Диапазон частот для кардионагрузки: от '+arr['pulse_2']+' до '+arr['pulse_3']+' уд/мин</p>';
    } else {
      pulse_1_msg='';
      pulse_err_flag = true;
    };

    if (arr['pulse_min'] && arr['pulse_max']) {
      var pulse_2_msg = '<p>Оптимальная частота сердцебиения: от '+arr['pulse_min']+' уд/мин до '+arr['pulse_max']+' уд/мин</p>';
    } else {
      pulse_2_msg='';
      pulse_err_flag = true;
    };

    if (!pulse_err_flag) {
      $('#pulse_body').addClass('bg-success');
    }

    if (!pulse_1_msg && !pulse_2_msg) {
      pulse_err_str = '<p>Недостаточно данных</p>' + pulse_err_str;
    };

    $('#pulse_content').html(pulse_1_msg + pulse_2_msg + pulse_err_str);

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

    // формируем отчет по телосложению
    if (arr['mass_size']) {
      var mass_size_msg = '';
      mass_size_msg += '<p>Ваше телосложение: <strong>' + arr['mass_size'] + '</strong></p>';
    } else {
      var mass_size_msg = '';
    };

    // формируем отчет по калориям
    var mass_cal_msg = '';
    if (arr['mass_rmr']) {
      mass_cal_msg += '<p>Метаболизм покоя: <strong>' + arr['mass_rmr'] + ' ккал в день</strong></p>';
    };

    if (arr['mass_calmin'] && arr['mass_imt']) {
      mass_cal_msg += '<p>Минимум потребления: <strong>' + arr['mass_calmin'] + ' ккал в день</strong></p>';
      if (arr['mass_imt'] >= 25) {
        mass_cal_msg += '<small><p>Ограничьте Вашу диету ' + Math.floor(arr['mass_calmin']*0.85) + ' ккалл в день, чтобы терять ' + Math.floor(arr['mass_calmin']*0.15*30/4086/2.2) + ' кг в месяц</p></small>';
      } else {
        mass_cal_msg += '';
      };
    } else {
      mass_err_flag = true;
    };

    if (arr['mass_aam']) {
      mass_cal_msg += '<p>Рекомендуемый метаболизм: <strong>' + arr['mass_aam'] + ' ккал в день</strong></p>';
    };

    // формируем отчет по белку
    if (arr['mass_protein']) {
      var mass_protein_msg = '';
      mass_protein_msg += '<p>Потребляйте примерно <strong>' + arr['mass_protein'] + ' г. белка в день</strong> <small>(' + (arr['mass_protein']/arr['weight']).toFixed(2) + ' грамм на кг.)</small>';
    } else {
      var mass_protein_msg = '';
      mass_err_flag = true;
    };

    if (!mass_imt_msg && !mass_2_msg && !mass_fat_msg && !mass_cal_msg && !mass_protein_msg && !mass_size_msg) {
      mass_err_str = '<p>Недостаточно данных</p>' + mass_err_str;
    };

    $('#mass_content').html(mass_imt_msg+mass_2_msg+mass_fat_msg+mass_cal_msg+mass_protein_msg+mass_size_msg+mass_err_str);
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
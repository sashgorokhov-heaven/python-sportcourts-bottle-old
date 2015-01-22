% import datetime
% rebase("_adminpage", title="Логи c {} по {}".format('{}-{}-1'.format(datetime.date.today().year, datetime.date.today().month), datetime.date.today()))
<div class="row">
  <div class="col-md-6">
    <div id="chart_div" style="width: 900px; height: 500px; max-width:100%;"></div>
  </div>
  <div class="col-md-6">
    <div id="dates_div" style="width: 900px; height: 500px; max-width:100%;"></div>
  </div>
</div>
<div class="row">
  <div class="col-md-6">
    <div id="probability_density_div" style="width: 900px; height: 500px; max-width:100%;"></div>
  </div>
  <div class="col-md-6">
    <div id="persent_growth_div" style="width: 900px; height: 500px; max-width:100%;"></div>
  </div>
</div>
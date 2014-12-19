% if defined("seo_info"):
% keywords = seo_info.keywords()
% description = seo_info.description()
% end

% import datetime

% setdefault("keywords", "")
% setdefault("description", "")
<title>{{title}} | SportCourts.ru</title>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8">
<meta name="keywords" content="{{keywords}}" />
<meta name="description" content="{{description}}" />
<meta name="time" content="{{datetime.datetime.now()}}" />
<meta http-equiv="X-UA-Compatible" content="IE=edge">
<meta name="viewport" content="width=600">

<meta name="google-site-verification" content="UiLEwcYPzjypS-khlrSkBr31Qr2xp-Qd1l0RVbzZ5Uc" />
<meta name="verify-reformal" content="bb4f4af81081a514619ba2c0" />

<link rel="icon" type="image/vnd.microsoft.icon" href="/images/static/favicon.ico" />

<script src="//ajax.googleapis.com/ajax/libs/jquery/2.1.1/jquery.min.js"></script>

<style>
  .topmenu-promo{
    background-image: linear-gradient(to bottom, rgb(200,15,25) 0, #222 100%) !important;
    color:#bbb;
    height:52px !important;
    margin-bottom: -2px !important;
  }
</style>

<style>
  #preloader  {
       position: absolute;
       top: 0;
       left: 0;
       right: 0;
       bottom: 0;
       background-color: #fefefe;
       z-index: 99;
      height: 100%;
   }

  #status  {
       width: 200px;
       height: 200px;
       position: absolute;
       left: 50%;
       top: 35%;
       background-image: url(http://w3lessons.info/demo/jquery-preloader/ajax-loader.gif);
       background-repeat: no-repeat;
       background-position: center;
       margin: -100px 0 0 -100px;
   }
</style>
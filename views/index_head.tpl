<meta property="og:title" content="SportCourts" />
<meta property="og:site_name" content="Site Name" />
<meta property="og:type" content="website" />
<meta property="og:url" content="http://{{serverinfo['ip']}}:{{serverinfo['port']}}"/>
<meta property="og:image" content="https://pp.vk.me/c620028/v620028278/1312a/jafmfIBHbVs.jpg" />
<meta property="og:description" content="Ваш проводник в мир любительского спорта. Огромная база спортивных событий для каждого! "/>

<script src="/view/js/typed.js"></script>

<script>
  $(function(){
    $(".gamestyped").typed({
      strings: ["футбол", "баскетбол", "волейбол"],
      typeSpeed: 170,
      backDelay: 600,
      loop: true,
      loopCount: false
    });
  });
</script>

<style>
  .typed-cursor{
      opacity: 1;
      -webkit-animation: blink 0.7s infinite;
      -moz-animation: blink 0.7s infinite;
      animation: blink 0.7s infinite;
  }
  @keyframes blink{
      0% { opacity:1; }
      50% { opacity:0; }
      100% { opacity:1; }
  }
  @-webkit-keyframes blink{
      0% { opacity:1; }
      50% { opacity:0; }
      100% { opacity:1; }
  }
  @-moz-keyframes blink{
      0% { opacity:1; }
      50% { opacity:0; }
      100% { opacity:1; }
  }

  .bigheadrow{
    height:100vh;
    max-height:800px;
  }

  .bighead{
    position:absolute;
    top:{{'45' if loggedin else '20'}}%;
    left:25%;
    z-index:30;
    width:50%;
    height: 100vh;
    max-height:800px;
    color: rgb(255, 255, 255);
    text-shadow: rgba(0, 0, 0, 0.6) 0px 1px 2px;
  }

  .item{
    background-color:black;
    height:100vh;
    max-height:800px;
  }

  .item img{
    min-height:100% !important;
    opacity:0.5;
  }

  .smallhead{
    padding-top:60px;
  }

  .indexpromo{
    padding-bottom: 30px;
  }
</style>
<link rel="stylesheet" href="/view/jasny/css/jasny-bootstrap.css">
<script src="/view/jasny/js/jasny-bootstrap.js"></script>

<link rel="stylesheet" href="/view/js/chosen/chosen.css">
<script src="/view/js/chosen/chosen.jquery.js"></script>

<script type="text/javascript">
    $('.fileinput').fileinput()
</script>

<script type="text/javascript">
  $('.typeahead').typeahead({
    source: [{{!', '.join(['"{}"'.format(i.title()) for i in cities])}}],
    items: {{len(cities)}},
    minLength: 1
  })
</script>

<script type="text/javascript">
  $('.phonemask').inputmask({
    mask: '+7 (999) 999 99 99'
  })
</script>

<style>
	.chosen-container{
		-webkit-appearance: none;
		-webkit-box-shadow: rgba(0, 0, 0, 0.0745098) 0px 1px 1px 0px inset;
		-webkit-rtl-ordering: logical;
		-webkit-transition-delay: 0s, 0s;
		-webkit-transition-duration: 0.15s, 0.15s;
		-webkit-transition-property: border-color, box-shadow;
		-webkit-transition-timing-function: ease-in-out, ease-in-out;
		-webkit-user-select: text;
		-webkit-writing-mode: horizontal-tb;
		background-color: rgb(255, 255, 255);
		background-image: none;
		border-bottom-color: rgb(204, 204, 204);
		border-bottom-left-radius: 4px;
		border-bottom-right-radius: 4px;
		border-bottom-style: solid;
		border-bottom-width: 1px;
		border-image-outset: 0px;
		border-image-repeat: stretch;
		border-image-slice: 100%;
		border-image-source: none;
		border-image-width: 1;
		border-left-color: rgb(204, 204, 204);
		border-left-style: solid;
		border-left-width: 1px;
		border-right-color: rgb(204, 204, 204);
		border-right-style: solid;
		border-right-width: 1px;
		border-top-color: rgb(204, 204, 204);
		border-top-left-radius: 4px;
		border-top-right-radius: 4px;
		border-top-style: solid;
		border-top-width: 1px;
		box-shadow: rgba(0, 0, 0, 0.0745098) 0px 1px 1px 0px inset;
		box-sizing: border-box;
		color: rgb(85, 85, 85);
		cursor: auto;
		display: block;
		font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
		font-size: 14px;
		font-style: normal;
		font-variant: normal;
		font-weight: normal;
		height: 34px;
		letter-spacing: normal;
		line-height: 20px;
		margin-bottom: 0px;
		margin-left: 0px;
		margin-right: 0px;
		margin-top: 0px;
		padding-bottom: 6px;
		padding-left: 2px;
		padding-right: 2px;
		padding-top: 2px;
		text-align: start;
		text-indent: 0px;
		text-shadow: none;
		text-transform: none;
		transition-delay: 0s, 0s;
		transition-duration: 0.15s, 0.15s;
		transition-property: border-color, box-shadow;
		transition-timing-function: ease-in-out, ease-in-out;
		word-spacing: 0px;
		writing-mode: lr-tb;
	}

	.chosen-choices{
		border-width: 0;
		width: 100%;
	}
</style>
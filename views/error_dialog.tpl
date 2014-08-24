<div class="error_dialog">
	<p class="bg-danger" style="padding:10px; margin-top: 40px;">{{error}}</p>
	% if error_description:
	<p class="bg-danger" style="padding:10px;">{{error_description}}</p>
	% end
	% if traceback:
	<p class="bg-danger" style="padding:10px;">{{traceback}}</p>
	% end
</div>
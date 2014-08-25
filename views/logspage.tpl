% rebase("_basicpage", title="Server logs")
<div class="container">
	<div class="row clearfix">
		<div class="col-md-12 column">
			<div class="page-header">
				<h1>
					Server logs
				</h1>
			</div>

            %for log in logs:
			    <div class="panel panel-{{log[0]}}">
			    	<div class="panel-heading">
			    		<h3 class="panel-title">
			    			{{log[1]}}
			    		</h3>
			    	</div>
			    	<div class="panel-body">
			    		{{log[2]}}
			    	</div>
			    	% if len(log)>3:
			    	    <div class="panel-footer">
			    	    	{{!'<br>'.join(log[3:])}}
			    	    </div>
			    	% end
			    </div>
			% end
		</div>
	</div>
</div>
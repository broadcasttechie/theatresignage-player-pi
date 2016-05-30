<html>
	<head>
		<title>Splash</title>
		<link href="./static/css/bootstrap.min.css" rel="stylesheet" />
		
		<style>
		body, :not(.well) { 
			background: #000000 !important;
			color: white;
		}
		.well {
			color: black
		
		}
		</style>
</html>
<body>
<div class="container">
	<div class="row">
		<div class="col-md-12">
			<div class="page-header text-center">
				<h1>Theatre Signage</h1>
				<small></small>
			</div>
		</div>
	</div>
	<div class="row">
		<div class="col-md-12">
			<p class="lead">
				Playlist server: {{server}}, channel: {{channel}}
			</p>
			<div class="well lead text-center">
				{{host}}:8080
			</div>
		</div>
	</div>
	<hr />
	<div class="row">
		<div class="col-md-12 text-right">
			Player ID: xxxxxx
		</div>
	</div>
</div>
<script src="static/js/bootstrap.min.js"
</body>
</html>
<html>
	<head>
		<title>Theatre Signage Settings</title>
		<link href="./static/css/bootstrap.min.css" rel="stylesheet" />
		
		<style>
		body, :not(.well) { 
			background: #white !important;
			color: black;
		}
		.well {
			color: white
		
		}
		</style>
		<script>
		setInterval(function() {
			var myImageElement = document.getElementById('thumb');
			myImageElement.src = '/screenshot/thumb?rand=' + Math.random();
		}, 2000);
		</script>
</html>
<body>
<div class="container">
	<div class="row">
		<div class="col-md-12">
			<div class="page-header text-center">
				<h1>Theatre Signage Configuration</h1>
				<small></small>
			</div>
		</div>
	</div>
	<div class="row">
		<div class="col-md-12">
			<p class="lead">
				
				<img src="/screenshot/thumb" id="thumb"/>
			</p>
			<div class="well lead text-center">
				<form class="form-horizontal" method="POST">
<fieldset>

<!-- Form Name -->
<legend>Settings</legend>

<!-- Text input-->
<div class="form-group">
  <label class="col-md-4 control-label" for="server">Server</label>  
  <div class="col-md-4">
  <input id="server" name="server" type="text" placeholder="ts.zamia.co.uk" value="{{server}}" class="form-control input-md" required="">
  <span class="help-block">Playlist server</span>  
  </div>
</div>

<!-- Text input-->
<div class="form-group">
  <label class="col-md-4 control-label" for="channel">Channel ID</label>  
  <div class="col-md-4">
  <input id="channel" name="channel" type="text" placeholder="2" value="{{channel}}" class="form-control input-md" required="">
  <span class="help-block">ID number of channel</span>  
  </div>
</div>
<div class="form-group">
  <label class="col-md-4 control-label" for="submit"></label>
  <div class="col-md-4">
    <button type="submit" id="submit" name="submit" class="btn btn-primary">Save</button>
  </div>
</div>
<fieldset>
<legend>
System Control
</legend>
<div class="form-group"><div class="col-md-4">
  <label class="col-md-4 control-label" for="submit"></label>
  <div class="col-md-4">
  <a class="btn btn-success" href="/reboot" role="button">reboot</a>
  <a class="btn btn-danger" href="/shutdown" role="button">shutdown</a>
  </div>
</div>
</div>

</form>
<hr />
<legend>
System Control
</legend>
<div class="form-group"><div class="col-md-4">
  <label class="col-md-4 control-label" for="submit"></label>
  <div class="col-md-4">
  <a class="btn btn-success" href="/reboot" role="button">reboot</a>
  <a class="btn btn-danger" href="/shutdown" role="button">shutdown</a>
  </div>
</div>
</div>




			</div>
		</div>
	</div>
	<hr />
	<div class="row">
		<div class="col-md-12 text-right">
			
		</div>
	</div>
</div>
<script src="static/js/bootstrap.min.js"
</body>
</html>
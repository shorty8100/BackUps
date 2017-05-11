<!DOCTYPE html>
<html lang="en">

<head>

<!-- title and meta -->
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width,initial-scale=1.0" />
<meta name="description" content="A simple slide down menu using jQuery and CSS" />
<title>Slide Down Menu With jQuery</title>
	
<!-- css -->
<link href='http://fonts.googleapis.com/css?family=Ubuntu:300,400,700,400italic' rel='stylesheet' type='text/css'>
<link href='http://fonts.googleapis.com/css?family=Oswald:400,300,700' rel='stylesheet' type='text/css'>
<link rel="stylesheet" href="css/base.css" />
<link rel="stylesheet" href="css/style.css" />
	
<!-- js -->
<script src="jquery-3.2.1.js"></script>
<script>
	$(document).ready(function() {
		$( '.dropdown' ).hover(
			function(){
				$(this).children('.sub-menu').slideDown(0);
			},
			function(){
				$(this).children('.sub-menu').slideUp(0);
			}
		);
	}); // end ready
</script>
<style>
nav { background-color:rgb(255,100,100); padding:10px 0; }
nav ul { list-style-type:none; margin:0; padding:0; }
nav ul li { display:inline-block; position:relative; }
nav li ul { background-color:rgb(225,75,75); position:absolute; left:0; top:40px; width:200px; }
nav li li { position:relative; margin:0; display:block; }
nav li li ul { position:absolute; top:0; left:200px; margin:0; }
nav a { line-height:40px; padding:0 12px; margin:0 12px; }
nav a { color:#fff; text-decoration:none; display:block; }
nav a:hover, nav a:focus, nav a:active { color:rgb(50,50,50); }
nav li li a { border-bottom:solid 1px rgb(200,50,50); margin:0 10px; padding:0; }
nav li li:last-child a { border-bottom:none; }
nav li.dropdown > a { background-image:url('arrow-down.png'); background-position:right 20px; background-repeat:no-repeat; }
nav li li.dropdown > a { background-image:url('arrow-right.png'); background-position:right 16px; background-repeat:no-repeat; }
ul.sub-menu { display:none; }
nav img { height: 16px; width: 16px; }
</style>
</head>

<body>

<div id="wrapper">

<header>
</header>

<nav>
	<ul class="content clearfix">
		<li><a href="#">Nav 1</a></li>
		<li><a href="#">Nav 2</a></li>
		<li class="dropdown">
			<a href="#"><img src="https://maxcdn.icons8.com/Share/icon/ios7/Cinema//anonymous_mask1600.png">Nav 3</a>
			<ul class="sub-menu">
				<li><a href="#">Nav 3.1</a></li>
				<li><a href="#">Nav 3.2</a></li>
				<li><a href="#">Nav 3.3</a></li>
				<li class="dropdown">
					<a href="#"><img src="https://maxcdn.icons8.com/Share/icon/ios7/Cinema//anonymous_mask1600.png">Nav 3.4</a>
					<ul class="sub-menu">
						<li><a href="#">Nav 3.4.1</a></li>
						<li class="dropdown">
							<a href="#">Nav 3.4.2</a>
							<ul class="sub-menu">
								<li><a href="#">Nav 3.4.2.1</a></li>
								<li><a href="#">Nav 3.4.2.2</a></li>
								<li><a href="#">Nav 3.4.2.3</a></li>
								<li><a href="#">Nav 3.4.2.4</a></li>
								<li><a href="#">Nav 3.4.2.5</a></li>
							</ul>
						</li>
						<li><a href="#">Nav 3.4.3</a></li>
						<li><a href="#">Nav 3.4.4</a></li>
						<li><a href="#">Nav 3.4.5</a></li>
					</ul>
				</li>
				<li><a href="#"><img src="https://maxcdn.icons8.com/Share/icon/ios7/Cinema//anonymous_mask1600.png">Nav 3.5</a></li>
			</ul>
		</li>
		<li><a href="#">Nav 4</a></li>
		<li><a href="#">Nav 5</a></li>
	</ul>
</nav>

<div id="main">
</div>


<footer>
</footer>



</div>


</body>
</html>

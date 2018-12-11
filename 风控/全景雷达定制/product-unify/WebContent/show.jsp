<%@ page language="java" contentType="text/html; charset=UTF-8"
	pageEncoding="UTF-8"%>
<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
<link rel="stylesheet" href="style/jquery.jsonview.css" />
<title>新颜征信</title>
<style>
html {
	height: 100%;
}

body {
	height: 100%;
	padding: 0;
	margin: 0;
}

#container {
	width: 460px;
	background-color: #f2eeee;
	margin-left: -230px;
	margin-top: -230px;
	position: absolute;
	top: 30%;
	left: 50%;
	overflow:hidden;
}
#picture {
	height: 250px;
	margin-top: 5px;
	text-align:center;
	background-color:#FFFFE0;
}
</style>
</head>
<body>
	<div id="container">
		<h2>返回结果：</h2>
		<div id="json-collapsed"></div>
	</div>
	

</body>
<script type="text/javascript" src="js/jquery.min.js"></script>
<script type="text/javascript" src="js/jquery.jsonview.js"></script>
<script type="text/javascript">
	var data =<%=request.getAttribute("result")%>;
	$(function() {
		$("#json-collapsed").JSONView(data, {
			collapsed : false,
			nl2br : true,
			recursive_collapser : true
		});
	});
</script>

</html>
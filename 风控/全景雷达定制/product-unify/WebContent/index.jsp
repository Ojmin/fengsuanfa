<%@ page language="java" contentType="text/html; charset=UTF-8"
	pageEncoding="UTF-8"%>
<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
<title>新颜征信</title>
</head>
<body>
	<center>

		<form method="post" action=CustomizeUnifyController>
			<table width="500" border="0" cellspacing="0" cellpadding="3">
				<tr>
					<th colspan="2" align="center" bgcolor="#FFFFFF">全景雷达定制版
					</th>
				</tr>
				<tr>
					<td bgcolor="#FFFFFF">
					<input name="urlType" type="hidden" id="urlType" value="Url" /></td>
				</tr>
				<tr>
					<td align="right" bgcolor="#FFFFFF">身份证号：</td>
					<td bgcolor="#FFFFFF">
					<input name="id_no" type="text" id="id_no"  /></td>
				</tr>
				<tr>
					<td align="right" bgcolor="#FFFFFF">姓名：</td>
					<td bgcolor="#FFFFFF">
					<input name="id_name" type="text" id="id_name"  /></td>
				</tr>
				<tr>
					<td align="right" bgcolor="#FFFFFF">产品类型：</td>
					<td bgcolor="#FFFFFF">
					<input name="product_type" type="text" id="product_type"  /></td>
				</tr>
				<tr>
					<td align="right" bgcolor="#FFFFFF">版本号：</td>
					<td bgcolor="#FFFFFF">
					<input name="versions" type="text" id="versions"  /></td>
				</tr>
				<tr>
					<td colspan="2" align="center" bgcolor="#FFFFFF"><input
						type="submit" name="Submit" value="提交" /></td>
				</tr>

			</table>
		</form>
	</center>

</body>
</html>
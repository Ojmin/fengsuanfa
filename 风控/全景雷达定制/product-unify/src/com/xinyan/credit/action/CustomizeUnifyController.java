package com.xinyan.credit.action;

import java.io.File;
import java.io.IOException;
import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.HashMap;
import java.util.Map;

import javax.servlet.ServletException;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

import com.xinyan.credit.Config;
import com.xinyan.credit.rsa.RsaCodingUtil;
import com.xinyan.credit.util.HttpUtils;
import com.xinyan.credit.util.SecurityUtil;

import net.sf.json.JSONObject;

public class CustomizeUnifyController extends HttpServlet{
	
	private static final long serialVersionUID = 1L;

	@Override
	protected void doGet(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
		this.doPost(req, resp);
	}
	
	
	@Override
	protected void doPost(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
		String url;
		String postString;
		
		
		
		/** 1、 商户号 **/
		String member_id = Config.getConstants().get("member.id");
		/** 2、终端号 **/
		String terminal_id = Config.getConstants().get("terminal.id");
	    /**请求地址**/
		String urlType = req.getParameter("urlType");
		
		Map<String,String> headers=new HashMap<String,String>();
		
		/**请求参数**/
		String id_no=req.getParameter("id_no");
		String id_name=req.getParameter("id_name");
		String versions=req.getParameter("versions");
		String product_type=req.getParameter("product_type");
		
		String trans_id=System.currentTimeMillis()+"";//订单号
		String trade_date=new SimpleDateFormat("yyyyMMddHHmmss").format(new Date());// 订单日期
		
		String XmlOrJson = "";
		
		Map<String,String> params=new HashMap<String,String>();		
		params.put("member_id",member_id );
		params.put("terminal_id",terminal_id );
		params.put("trans_id",trans_id );
		params.put("trade_date",trade_date );
		params.put("id_no", id_no);
		params.put("id_name",id_name );
		params.put("product_type",product_type );
		params.put("versions",versions );
		params.put("industry_type", "A1");
		
		JSONObject jsonforMap=JSONObject.fromObject(params);
		XmlOrJson=jsonforMap.toString();
		log("====请求明文:" + XmlOrJson);
		
		/**base64加密**/
		String base64Str=SecurityUtil.Base64Encode(XmlOrJson);
		
		/**rsa加密**/
		String pfxpath = Config.getWebRoot() + "key\\" + Config.getConstants().get("pfx.name");// 商户私钥
		File pfxfile = new File(pfxpath);
		if (!pfxfile.exists()) {
			log("私钥文件不存在！");
			throw new RuntimeException("私钥文件不存在！");
		}
		String pfxpwd = Config.getConstants().get("pfx.pwd");// 私钥密码

		String data_content = RsaCodingUtil.encryptByPriPfxFile(base64Str, pfxpath, pfxpwd);// 加密数据
		
		url = Config.getConstants().get(urlType);
		log("url:" + url);
		Map<String,Object> inputParams=new HashMap<String,Object>();
		inputParams.put("member_id", member_id);
		inputParams.put("terminal_id", terminal_id);
		inputParams.put("data_type", "json");
		inputParams.put("data_content", data_content);
		
		postString = HttpUtils.doPost(url, headers,inputParams);
		log("请求返回：" + postString);
		
		/** ================处理返回结果============= **/
		if (postString.isEmpty()) {// 判断参数是否为空
			log("=====返回数据为空");
			throw new RuntimeException("返回数据为空");
		}
		req.setAttribute("result", postString);
		req.getRequestDispatcher("/show.jsp").forward(req, resp);
	}
	
	


	
	public void log(String msg) {
		System.out.println(new SimpleDateFormat("yyyy-MM-dd HH:mm:ss").format(new Date()) + "\t: " + msg);
	}
}

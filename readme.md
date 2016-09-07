##browser_vuln_check
---

`browser_vuln_check` ,利用已知的浏览器漏洞PoC 来快速检测Webview 和浏览器环境是否存在安全漏洞,检测原理是`run.html` 接收`<iframe>` 内嵌的PoC 页面返回的信息来判断WebView 是否存在漏洞<br/>
Example:<br/><br/>

    <body>
        <div id="output_state_window"></div>
        <iframe src="bad_kernel.html" style="visibility:hidden;"></iframe>
        <iframe src="oob.html" style="visibility:hidden;"></iframe>
        <iframe src="reflected_xss.html" style="visibility:hidden;"></iframe>
        <iframe src="access_port.html" style="visibility:hidden;"></iframe>
        <iframe src="uxss/exploit.html" style="visibility:hidden;"></iframe>
    </body>

通过`<iframe>` 给PoC 页面构造新的浏览器执行环境,使得PoC 页面内执行的检测漏洞代码互不影响,PoC 页面分为两部分:**post_result** 和**check_vuln** <br/>
Example:<br/><br/>

    function post_result(check_state) {  //  当前PoC 页面往上提交(run.html )检测结果
        var parentwin = window.parent;
        parentwin.postMessage(check_state,"*");
    }
    
    function check_vuln() {  //  开始检测漏洞
        var kMessages;
        Object.prototype.__defineGetter__("observe_accept_invalid",function(){
            log("called");
            kMessages=this});
        try{Object.observe({},function(){},1)}catch(e){}
        delete Object.prototype["observe_accept_invalid"];

        if (undefined!=kMessages)
            return true;
        return false;
    }
    post_result('({vuln_name:"bad_kernel",check_state:'+check_vuln()+'})');  //  向run.html 返回执行结果,包含漏洞名称和漏洞检测结果

在QQ 浏览器9.4.2 上的执行结果(`repoter_receiver.py` 提供了一种从WebView 扫描漏洞的结果返回到漏洞扫描器的方式,在APP 安全扫描器里只需要把`run.html` 导入到WebView 然后再到本地启动端口获取执行结果即可):<br/><br/>
![run_state](https://raw.githubusercontent.com/lcatro/browser_vuln_check/master/run_state.png)


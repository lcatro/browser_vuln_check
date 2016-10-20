## browser_vuln_check


`browser_vuln_check` 利用已知的浏览器漏洞PoC 来快速检测Webview 和浏览器是否存在安全漏洞,帮助产品上线之前检测公开的CVE 漏洞,减少外报漏洞漏水报告<br/>

---

### 怎么使用

如果你的电脑上没有安装`tornado` 库,第一步先安装目录`/depandent_python_lib` 下的`setuptools-28.6.0` ,然后再安装`tornado-master` <br/>

---

### 检测原理

`browser_vuln_check` 分两种类型的漏洞检测:崩溃和非崩溃型PoC 漏洞检测<br/><br/>

常见的非崩溃型漏洞检测包含:UXSS ,XSS 过滤器绕过,CSP 绕过,信息泄漏,其他小Bug 等检测,检测原理是通过`run.html` 接收`<iframe>` 内嵌的PoC 页面返回的信息来判断WebView 是否存在漏洞<br/>
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
![run_state](https://raw.githubusercontent.com/lcatro/browser_vuln_check/master/run_state.png)<br/><br/>

崩溃型PoC 采用Pydbg 调试进程,把url 传递给浏览器访问崩溃PoC ,直到浏览器崩溃时定位到崩溃点并获取上下文信息,由于现在浏览器大部分采用多进程运行,于是调试器并不方便针对浏览器的子进程来调试,所以在当前版本的`browser_vuln_check` 会把每一个会崩溃的PoC URL 作为参数来启动浏览器,然后等待执行结果,关闭浏览器,再执行下一个PoC <br/>

*WARNING!* `browser_vuln_check` 对于以*大写字母POC 或者CVE* 开头的文件,`server.py` 会认为这是一个有效的PoC 文件,作为\<iframe\> 添加到`run.html` 和`crash_poc_valid_logic.py` 中..<br/>

---

### PoC 构造

关于PoC 的构造在`uncrash_poc/_poc_temple.html` 下有PoC 的模板代码,`_poc_temple.html` 分为两部分:<br/>

        VULN_NAME='poc_temple';     //  PoC CVE ID or Name 
        VULN_VERSION=[];            //  PoC effect version 
                                    //  -> VULN_VERSION=None is unknow version ,
                                    //     VULN_VERSION=[]   is all version
                                    //     VULN_VERSION=['Chrome 50.0','Chrome 51.0.2344.1','QQ Browser 9316','Wechat 6.3.0-Wechar 6.3.12']  version detail

第一部分标记当前的PoC 的名字,版本.在进行漏洞扫描的时候,目的程序的版本对于漏洞分析和检测来说尤其重要,所以这个PoC 代码会影响到哪些版本我们也需要注意,这些信息最后能够帮助我们输出更加有说服力的检测报告<br/>

        function post_result(check_state) {
            var parentwin = window.parent;
            var post_result_json={};
            post_result_json.vuln_name=VULN_NAME;
            post_result_json.vuln_version=VULN_VERSION;
            post_result_json.vuln_valid_state=check_state;
            
            parentwin.postMessage(post_result_json,'*');
        }
        
        
        function check_vuln() {
            /////
            post_result(true);
        }
        
        check_vuln();
        
第二部分为PoC 的主要代码,`post_result()` 函数提供一个方便的接口,当我们在`check_vuln()` 中验证PoC 之后,下一步就应该把扫描的结果上报到`run.html` ,在这里你可以直接通过`post_result(true)` 或者`post_result(false)` 返回扫描结果,精简PoC 代码<br/><br/>

Example (`CVE-2016-1677`):<br/>

    VULN_NAME='CVE-2016-1677';                      //  CVE-ID
    VULN_VERSION=['Chrome 50-51','Wechat 6.3'];
    
    function post_result(check_state) {
        var parentwin = window.parent;
        var post_result_json={};
        post_result_json.vuln_name=VULN_NAME;
        post_result_json.vuln_version=VULN_VERSION;
        post_result_json.vuln_valid_state=check_state;

        parentwin.postMessage(post_result_json,'*');
    }
        
    
    function check_vuln() {
        var num = new Number(10);
        Array.prototype.__defineGetter__(0,function(){
            return num;
        })
        Array.prototype.__defineSetter__(0,function(value){
        })
        
        var str=decodeURI("%E7%9A%84");
        
        if (str.charCodeAt(0).toString(16)!='7684')  //  valid PoC
            post_result(true);                       //  Get it ..
        else
            post_result(false);
    }
        
    check_vuln();                                    //  Ready to valid PoC ..

这里需要注意一点,PoC 模板代码也分为两部分:`常用PoC` 和`UXSS` ,对于`UXSS` ,在调试的过程中发现并不是*100%* 可以准确验证这一类型的漏洞,后来发现通过`新建TAB 标签`可以提升UXSS 类漏洞的检测成功率,对于UXSS 这类漏洞,PoC 的检测机制如下:<br/>
 
![run_state](https://raw.githubusercontent.com/lcatro/browser_vuln_check/master/uxss_check_model.png)<br/>

首先,`run.html` 中包含的PoC \<iframe\> 是一个中转页面,然后通过这个中转页面新建一个TAB 标签,TAB 标签里面是我们的UXSS PoC 代码,实例如下(`CVE-2016-1697` ):<br/>

    window.onmessage=function(message) {
        if ('boolean'==typeof message.data) {
            check_is_valid_state=message.data;

            post_result(check_is_valid_state);
            new_tab.close();
        }
    }

    var new_tab=window.open('uncrash_poc?poc_name=_CVE-2016-1697.html');

在新标签里,浏览器总算提供了一个相对跟干净的环境给UXSS PoC 来执行验证,所以在新标签窗口中验证完成结果之后,把验证结果postMessage 到\<iframe\> 窗口,最后\<iframe\> 再往上传递到`run.html`<br/>


GitAutoDeploy
=============
简要说明：
----

* 使用Flask开发
* 只支持POST方法，因为GITLAB的webhook使用的post请求
* 判断本地目录是否存在.git目录，如果存在则执行`fetch`操作，如果不存在则进行`clone`操作
* 如果想要在`fetch`后执行个人的命令的话打开代码跳转到61行，然后增加你的命令即可

注意
---
请确保`url`和`path` 是一样的，否则会同步失败

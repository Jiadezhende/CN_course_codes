# Notes for Part2

## Web Crawling with Selenium and BrowserMob Proxy

❗可能遇到的问题

- 某些网站会强制 HTTPS，使用 http://{domain} 会导致超时或跳转失败
- BrowserMob Proxy 经常报 timeout / SSL handshake error
- Selenium 加载时间设置为 5 秒，许多网站加载不过来
- HAR 没有加延时，有些请求还没完成就写文件
- 没有处理 DNS 失败、证书错误、重定向
- 对失败网站没有自动跳过，仅靠异常继续可能导致 0/100 成功
- har/ 目录需要提前创建，否则写文件报错
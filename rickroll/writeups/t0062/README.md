# Rick roll [492 pts]

8-11-2020 :: T0062 - CUHK
Solved on November 7th, 9:53:10 PM
```
Author 作者：blackb6a

Description 描述：

Victoria, a friend of Dr Ke, is trying to build a new website. She is not familiar with it and didn't set any password protection yet. Can you find Victoria's secret?

維多利亞是奇異博士的朋友。她正在建設一個新的網站但未有設立密碼。你能找到維多利亞的秘密嗎？

http://tertiary.pwnable.hk:50007
```
## Solution
Upon visiting `http://tertiary.pwnable.hk:50007`, we were immediately rick rolled.

![rick-roll-0.png](https://www.dropbox.com/s/ryznceyw7dquho7/rick-roll-0.png?dl=0&raw=1)



There are a few possible ways to achieve this redirection. We decide to examine what happens exactly when we connect to `http://tertiary.pwnable.hk:50007`, using `curl`.

```bash
$ curl http://tertiary.pwnable.hk:50007 -v

*   Trying 18.163.58.67:50007...
* Connected to tertiary.pwnable.hk (18.163.58.67) port 50007 (#0)
> GET / HTTP/1.1
> Host: tertiary.pwnable.hk:50007
> User-Agent: curl/7.73.0
> Accept: */*
> 
* Mark bundle as not supporting multiuse
< HTTP/1.1 302 Found
< Date: Sun, 08 Nov 2020 15:05:08 GMT
< Server: Apache/2.4.38 (Debian)
< X-Powered-By: PHP/7.2.34
< Location: https://www.youtube.com/watch?v=dQw4w9WgXcQ&ab_channel=RickAstleyVEVO
< Content-Length: 0
< Content-Type: text/html; charset=UTF-8
< 
* Connection #0 to host tertiary.pwnable.hk left intact
```

The redirection is achieved using [HTTP Location Header](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Location). No further responses are provided.

The URL structure is `protocol://domain-name.top-level-domain/path`. Usually, this kind of redirection is only applied on the root path (`http://tertiary.pwnable.hk:50007/`). If we provide something for `path`, we shall get some interesting results (e.g. `404 Not Found`):

![rick-roll-1.png](https://www.dropbox.com/s/tbed0i9pmr2pswy/rick-roll-1.png?dl=0&raw=1)

This is a good sign. We can now try to find some resources that exist on the server. `robots.txt` and `sitemap.xml` are two frequently used files to describe the content of the website for web scrapers. `robots.txt` is found on this service.

![rick-roll-2.png](https://www.dropbox.com/s/ogtiyid04yi6ay0/rick-roll-2.png?dl=0&raw=1)

This suggests that we can access `http://tertiary.pwnable.hk:50007/b5HCLDptFQ6ZIZzw/flag.php` for flag. When we access that path, we were prompted for a HTTP basic authentication, which is weird since the description says that Victoria has not set up any password for the server.

![rick-roll-3.png](https://www.dropbox.com/s/axagsricpu9yst6/rick-roll-3.png?dl=0&raw=1)

So we try to use common credentials like `user/password`, `admin/admin`, etc. But no luck. The server always return `500 Internal Server Error` after entering the credentials.

We could not figure out what this means for a while. The `500 Internal Server Error` together with the challenge description seems very suspicious, as they strongly point to the fact that our goal is not to log in to the service with valid credentials. There may not even be a valid one for us to log in. (Note: `500 Internal Server Error` was strange because the server should return `401 Unauthorized` for incorrect credentials.)

Having decided that a dictionary attack for credentials would be useless, we looked at other elements in HTTP. We tried other HTTP methods (e.g. `POST`, `PUT`, `OPTIONS`), but either the method is not allowed, or the basic auth is still blocking our way.

Some time later our team member made a typo, and sent a `PUTS` request (NOT a valid method) to the server, which reveals the flag:

```bash
$ curl http://tertiary.pwnable.hk:50007/b5HCLDptFQ6ZIZzw/flag.php -X PUTS 
Congraulations! You get the flag.<br>hkcert{misc0nfiguration_0f_htacc3ss_is_fata1}
<script>
setTimeout(function () {
   window.location.href= 'https://www.youtube.com/watch?v=gkTb9GP9lVI&ab_channel=JwHDify';
}, 5000);
</script>                                            
```

The challenge ends here, but we decided to take a closer look. Turns out that any invalid methods would produce the same result. Even if you send `ABCD` as request method, the server would return the hidden content.

This also explains the `500 Internal Server Error` we saw before. Seems like the description is really speaking the truth, and there are no valid configuration files for the the authentication we came across. This should be the reason that the server didn't reject our wrong methods with  `405 Method Not Allowed`, and responded us with the hidden contents.

```
flag: hkcert{misc0nfiguration_0f_htacc3ss_is_fata1}
```

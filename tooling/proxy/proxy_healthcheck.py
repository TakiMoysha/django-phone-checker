import ssl, httpx


def test_request():
    ssl_ctx = ssl.SSLContext(protocol=ssl.PROTOCOL_TLSv1_2)
    ssl_ctx.set_alpn_protocols(["h2", "http/1.1"])
    ssl_ctx.set_ecdh_curve("prime256v1")
    ssl_ctx.set_ciphers(
        "ECDHE-RSA-AES256-GCM-SHA384:DHE-RSA-AES256-GCM-SHA384:"
        "ECDHE-ECDSA-CHACHA20-POLY1305:ECDHE-RSA-CHACHA20-POLY1305:"
        "DHE-RSA-CHACHA20-POLY1305:ECDHE-ECDSA-AES128-GCM-SHA256:"
        "ECDHE-RSA-AES128-GCM-SHA256:DHE-RSA-AES128-GCM-SHA256:"
        "ECDHE-ECDSA-AES256-SHA384:ECDHE-RSA-AES256-SHA384:"
        "DHE-RSA-AES256-SHA256:ECDHE-ECDSA-AES128-SHA256:"
        "ECDHE-RSA-AES128-SHA256:DHE-RSA-AES128-SHA256:"
        "ECDHE-ECDSA-AES256-SHA:ECDHE-RSA-AES256-SHA:"
        "DHE-RSA-AES256-SHA:ECDHE-ECDSA-AES128-SHA:"
        "ECDHE-RSA-AES128-SHA:DHE-RSA-AES128-SHA:"
        "RSA-PSK-AES256-GCM-SHA384:DHE-PSK-AES256-GCM-SHA384:"
        "RSA-PSK-CHACHA20-POLY1305:DHE-PSK-CHACHA20-POLY1305:"
        "ECDHE-PSK-CHACHA20-POLY1305:AES256-GCM-SHA384:"
        "PSK-AES256-GCM-SHA384:PSK-CHACHA20-POLY1305:"
        "RSA-PSK-AES128-GCM-SHA256:DHE-PSK-AES128-GCM-SHA256:"
        "AES128-GCM-SHA256:PSK-AES128-GCM-SHA256:AES256-SHA256:"
        "AES128-SHA256:ECDHE-PSK-AES256-CBC-SHA384:"
        "ECDHE-PSK-AES256-CBC-SHA:SRP-RSA-AES-256-CBC-SHA:"
        "SRP-AES-256-CBC-SHA:RSA-PSK-AES256-CBC-SHA384:"
        "DHE-PSK-AES256-CBC-SHA384:RSA-PSK-AES256-CBC-SHA:"
        "DHE-PSK-AES256-CBC-SHA:AES256-SHA:PSK-AES256-CBC-SHA384:"
        "PSK-AES256-CBC-SHA:ECDHE-PSK-AES128-CBC-SHA256:ECDHE-PSK-AES128-CBC-SHA:"
        "SRP-RSA-AES-128-CBC-SHA:SRP-AES-128-CBC-SHA:RSA-PSK-AES128-CBC-SHA256:"
        "DHE-PSK-AES128-CBC-SHA256:RSA-PSK-AES128-CBC-SHA:"
        "DHE-PSK-AES128-CBC-SHA:AES128-SHA:PSK-AES128-CBC-SHA256:PSK-AES128-CBC-SHA"
    )
    user_agent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36"

    socks_proxy = "socks5://178.141.240.140:1080"
    http_proxy = "http://185.221.160.176:80"
    client = httpx.Client(http2=True, verify=ssl_ctx, proxy=http_proxy)

    http_url = "http://opendata.digital.gov.ru/registry/numeric/downloads/"
    res = client.get(
        http_url,
        headers={
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "en-US,en;q=0.5",
            "Connection": "keep-alive",
            "Host": "opendata.digital.gov.ru",
            "Upgrade-Insecure-Requests": "1",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "none",
            "Sec-Fetch-User": "?1",
            "TE": "trailers",
            "User-Agent": user_agent,
            "Cookie": "",
        },
    )
    print(res.text)
    print(res, res.cookies)


if __name__ == "__main__":
    test_request()

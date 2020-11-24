# -*- coding: UTF-8 -*-
import socks
# Формирование проксисерверов

# Какой-то проксисервер
def outer_proxy():
    # http://spys.one/europe-proxy/ для поиска Proxy. Работоспособность proxy проверяется на десктопной версии
    host = "163.172.146.119"
    port = 8811
    #proxy = (socks.SOCKS5, host, port)
    proxy = (socks.HTTP, host, port)
    return (socks.HTTP, host, port)

# Наш проксисервер
def inner_proxy():
    host = "10.7.1.85"
    port = 1080
    return (socks.SOCKS5, host, port)
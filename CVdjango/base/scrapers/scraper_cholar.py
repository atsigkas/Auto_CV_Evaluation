from scholarly import scholarly, ProxyGenerator

def proxy():
    pg = ProxyGenerator()
    success = pg.FreeProxies()
    scholarly.use_proxy(pg)


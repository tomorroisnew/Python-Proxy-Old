from proxy import TcpSSLProxy
import callback
from importlib import reload

callbackFunction = callback.callback

def executeCallback(data, toServer):
    return callbackFunction(data, toServer)

proxy = TcpSSLProxy('10.10.10.10', 443, '10.10.10.10', 443, 'certs/server.crt', 'certs/server.key', intercept_callback=executeCallback)
proxy.start()
while True:
    try:
        reload(callback)
        callbackFunction = callback.callback
    except Exception as e:
        print(e)
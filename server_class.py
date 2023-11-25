from server_authenticate import ServerAuthenticator
from request import Request

class Server():
    def __init__(self,server_ip,server_port,username,password):
        self.url=f'http://{server_ip}:{server_port}'
        self.authenticator=ServerAuthenticator(url=self.url,username=username,password=password)
        self.cookie=self.authenticator.get_cookie()
        self.request=Request(cookie=self.cookie.get_dict())
        
        
    def get_configs(self):
        url=f'{self.url}/xui/inbounds/'
        response = self.request.post_protected_request(url=url).json()["obj"]
        return response
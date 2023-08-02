from request import Request

class ServerAuthenticator:
    def __init__(self,url,username,password):
            self.url=url
            self.username=username
            self.password=password
            self.header={    'Accept': 'application/json, text/plain, */*',
                            'Accept-Language': 'en-US,en;q=0.9',
                            'Connection': 'keep-alive',
                            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                            'Sec-Fetch-Dest': 'empty',
                            'Sec-Fetch-Mode': 'cors',
                            'Sec-Fetch-Site': 'same-origin',}
            self.request=Request()
    def get_cookie(self):
        response=self.request.post_request(url=f'{self.url}/login',
                                  body={"username":self.username,"password":self.password})
        return response.get_response_cookie()
        
        
        
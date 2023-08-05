import requests

class Request():
    def __init__(self,cookie=None):
        self.headers={
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'en-US,en;q=0.9',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Pragma': 'no-cache',
        }
        self.cookie=cookie
        if cookie:
            self.cookie={**self.cookie,'lang': "en-US"}
            

    def post_protected_request(self,url,body=None):
        if self.cookie==None :
                raise "should insert cookie"
        response = requests.post(url, cookies=self.cookie,
                headers=self.headers, verify=False,data=body)
        return ResponseFormat(response)
    
    def post_request(self,url,body=None):
        r=requests.session()
        response = r.post(url,headers=self.headers, verify=False,data=body)
        return ResponseFormat(response)
    def get_protected_request(self,url):
        if self.cookie==None :
                raise "should insert cookie"
        response = requests.get(url, cookies=self.cookie,
                headers=self.headers, verify=False)
        return ResponseFormat(response)

    def get_request(self,url):
        response = requests.get(url,headers=self.headers, verify=False)
        return ResponseFormat(response)
    
class ResponseFormat():
    def __init__(self, response):
        self.response=response
        
    def json(self):
        return self.response.json()
    def get_response_cookie(self):
        return self.response.cookies
    def get_response(self):
        return self.response